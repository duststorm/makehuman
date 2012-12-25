import os
import urllib2
import mh
from threading import Thread
import log

class MediaSync(Thread):
    
    def __init__(self, app, path, url, callback=None):
        
        Thread.__init__(self)
        self.app = app
        self.path = path
        self.url = url
        self.callback = callback
        
    def run(self):
        
        cache = DownloadCache(self.path)
        mh.callAsync(lambda:self.app.progress(0.0, 'Downloading media list'))
        success, code = cache.download(os.path.join(self.url, 'media.ini'))
        if success:
            f = open(os.path.join(self.path, 'media.ini'), 'r')
            filenames = f.readlines()
            n = float(len(filenames))
            for index, filename in enumerate(filenames):
                try:
                    filename = filename.split()[0]
                    mh.callAsync(lambda:self.app.progress(index/n, 'Downloading %s' % filename))
                    url = os.path.join(self.url, filename)
                    success, code = cache.download(url)
                except:
                    pass
            f.close()
            mh.callAsync(lambda:self.app.progress(1.0))
        else:
            mh.callAsync(lambda:self.app.progress(1.0))
            mh.callAsync(lambda:self.app.prompt('Error', 'Failed to sync media from %s, error %d.' % (self.path, code), 'OK'))
            
        if self.callback:
             mh.callAsync(self.callback)

class DownloadCache():

    class NotModifiedHandler(urllib2.BaseHandler):
  
        def http_error_304(self, req, fp, code, message, headers):
            
            addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
            addinfourl.code = code
            
            return addinfourl
        
    def __init__(self, path):
    
        self.path = path
            
        cachePath = os.path.join(self.path, 'cache.ini')
        if os.path.exists(cachePath):
            f = open(cachePath, 'r')
            self.cache = eval(f.read(), {"__builtins__":None}, {'True':True, 'False':False})
            f.close()
        else:
            self.cache = {}
            
    def download(self, url):
        
        filename = os.path.basename(url)
        
        if os.path.exists(os.path.join(self.path, filename)):
            etag, modified = self.cache.get(filename, (None, None))
        else:
            etag, modified = None, None
        
        try:
            downloaded, etag, modified, data = self.__downloadConditionally(url, etag, modified)
        except urllib2.HTTPError, e:
            log.notice('Could not download %s: %s', url, e)
            return False, e.code
                
        if downloaded:
            f = open(os.path.join(self.path, filename), 'wb')
            f.write(data)
            f.close()
            self.cache[filename] = (etag, modified)
            
        cachePath = os.path.join(self.path, 'cache.ini')
        f = open(cachePath, 'w')
        f.write(repr(self.cache))
        f.close()
        
        return True, (200 if downloaded else 304)
        
    @classmethod
    def __downloadConditionally(cls, url, etag=None, modified=None):
    
        request = urllib2.Request(url)
        
        if etag:
            request.add_header("If-None-Match", etag)
      
        if modified:
            request.add_header("If-Modified-Since", modified)
     
        opener = urllib2.build_opener(cls.NotModifiedHandler())
        handle = opener.open(request)
        headers = handle.info()
     
        if hasattr(handle, 'code') and handle.code == 304:
            return False, None, None, None
        else:
            return True, headers.getheader("ETag"), headers.getheader("Last-Modified"), handle.read()

#!/usr/bin/env python
import sys
sys.path.append("./core")
sys.path.append("./lib")
import algos3d
import os
import zipfile

if __name__ == '__main__':
    obj = algos3d.Target(None, None)
    with zipfile.ZipFile('data/targets.npz', mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk('data'):
            for name in files:
                try:
                    base, ext = os.path.splitext(name)
                    ext = ext.lower()
                    if ext != '.target':
                        continue
                    path = os.path.join(root, name)
                    obj._load_text(path)
                    iname, vname = obj._save_binary(path)
                    zip.write(iname)
                    zip.write(vname)
                    os.remove(iname)
                    os.remove(vname)
                except StandardError, e:
                    log.error('converting target %s', name, exc_info=True)

    with open('data/images.list', 'w') as f:
        for root, dirs, files in os.walk('data/targets'):
            for name in files:
                base, ext = os.path.splitext(name)
                ext = ext.lower()
                if ext != '.png':
                    continue
                path = os.path.join(root, name).replace('\\','/')
                f.write(path + '\n')

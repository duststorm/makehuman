import os.path
from scipy.linalg import pinv,svd
from scipy.spatial import KDTree
from scipy.optimize import leastsq
import numpy as np
import os

def rotX(angle):
    cosa = np.cos(angle)
    sina = np.sin(angle)
    
    return np.array(
        [[ 1.0 ,   0.0 ,   0.0 ],
         [ 0.0 ,  cosa ,  sina ],
         [ 0.0 , -sina ,  cosa ]])

def rotY(angle):
    cosa = np.cos(angle)
    sina = np.sin(angle)
    
    return np.array(
        [[  cosa , 0.0  ,-sina ],
         [   0.0 , 1.0  ,  0.0 ],
         [  sina , 0.0  , cosa]])

def rotZ(angle):
    cosa = np.cos(angle)
    sina = np.sin(angle)

    return np.array(
        [[  cosa , sina ,  0.0 ],
         [ -sina , cosa ,  0.0 ],
         [   0.0 ,  0.0 ,  1.0 ]])

def rot(alpha,beta,gamma):
    return np.dot(rotZ(gamma),np.dot(rotY(beta),rotZ(alpha)))

def find_transform(mask_scan,mask_mh):
    """
        Computes the transformation to align mask_scan
        and mask_mh.
        
        mask_scan' = scale * R * mask_scan + T
        
        arguments :
            mask_scan, mask_mh : 2D arrays where each row contains
                      the 3D coordinate of a vertex. Vertices in
                      mask_scan and mask_mh are assumed to be in the
                      same order.
                      
        returns :
            (scale,R,T)
            scale : the scaling factor.
            R : the rotation matrix
            T : the translation
            
    """
    
    mask_scan = np.array(mask_scan)
    mask_mh = np.array(mask_mh)
    
    def loss(transform):
        alpha,beta,gamma,scale,tx,ty,tz = transform
        verts = apply_transform(scale,(alpha,beta,gamma),(tx,ty,tz),mask_scan)
        return (mask_mh - verts).flatten()

    tr0 = [0.0,0.0,0.0,1.0,0.0,0.0,0.0]
    res = leastsq(loss,tr0)[0]
    alpha,beta,gamma,scale,tx,ty,tz = res
    return scale,(alpha,beta,gamma),(tx,ty,tz)


def apply_transform(scale,R,T,vertices,center = None):
    """
        Apply the transformation 
        x' = scale*R*x + T
        for each point in points (one point per row).
    """
    mean = np.mean(vertices,0) if center is None  else center
    return scale*np.dot(vertices-mean,rot(*R).T) + mean + T

def align_scan(mask_scan,mask_mh,scan):
    """
        Align 'scan' using mask_scan and mask_mh.
        
        mask_scan, mask_mh, and scan are 2D arrays
        with one 3d point per row
    """
    scale,R,T = find_transform(mask_scan,mask_mh)
    return apply_transform(scale,R,T,scan,center = np.mean(mask_scan,0)),apply_transform(scale,R,T,mask_scan)


class TargetBase(object):
    """
        Object used to manage target projection bases.
        
        important attributes are :
        - names : list of target names. This can be used for creating
                  the combinaison of targets to use (boddy setting files)
        - vert_list : the vertices that will be used. 
        - targets : the targets as a 3D array (ntargets,nvertices,3)
        - prefix  : prefix used to load or save the different components
                    of the base.
    
    """
    def __init__(self,names = None,vert_list=None,targets=None,prefix = None):
        self._names = names
        self._vert_list = vert_list
        self._targets = None if targets is None else np.array(targets)

        if targets is None :
            self._u = self._s = self._vt = None
        else :
            print "Computing svd decomposition..."
            ntargs,nverts,dim = targets.shape
            targets = targets.reshape(ntargs,nverts*dim)
            self._u,self._s,self._vt = svd(targets.T,full_matrices = False)
            print "OK"

        self.prefix = prefix

    @property
    def u(self):
        if self._u is None and self.prefix is not None :
            self._u  = np.load(self.prefix+"_u.npy")
        return self._u

    @property
    def s(self):
        if self._s is None and self.prefix is not None :
            self._s  = np.load(self.prefix+"_s.npy")
        return self._s

    @property
    def vt(self):
        if self._vt is None and self.prefix is not None :
            self._vt  = np.load(self.prefix+"_vt.npy")
        return self._vt

    @property
    def vert_list(self):
        if self._vert_list is None and self.prefix is not None :
            try :
                self._vert_list  = np.loadtxt(self.prefix+".verts",'int')
            except IOError : pass
        return self._vert_list
    
    @property
    def targets(self):
        if self._targets is None and self.prefix is not None :
            self._targets  = np.load(self.prefix+"_targets.npy")
        return self._targets

    @property
    def names(self):
        if self._names is None and self.prefix is not None :
            with open(prefix+".names","r") as f :
                self._names = [ l.strip() for l in f]
        return self._names

    def save(self,prefix = None):
        if prefix is not None : self.prefix = prefix

        with open(self.prefix+".names","w") as f :
            f.write("\n".join(self.names)+"\n")
        
        if self.vert_list is not None : np.savetxt(self.prefix+".verts",self.vert_list,"%i")
        np.save(self.prefix+"_targets.npy",self.targets)
        np.save(self.prefix+"_u.npy",self.u)
        np.save(self.prefix+"_s.npy",self.s)
        np.save(self.prefix+"_vt.npy",self.vt)

    def project_target(self,target,rcond = 0.0):
        """
            Rebuild 'target' as a combinaison of 'targets' using 'u'.
            t' = u* u.T * t
            
            arguments :
            - target : target to fit
            - rcond : cut off on the singular values as a fraction of
                      the biggest one. Only base vectors corresponding
                      to singular values bigger than rcond*largest_singular_value
        """
        
        u = self.u[ : , self.s>= rcond*self.s[0]]
        
        if not isinstance(target,np.ndarray) :
            target = np.array(target)
        if target.ndim == 2 :
            nverts,dim = target.shape
            target = target.reshape(nverts*dim)
            return np.dot(np.dot(target,u),u.T).reshape(nverts,dim)
        else :
            ntargs,nverts,dim = target.shape
            target = target.reshape(ntargs,nverts*dim)
            return np.dot(np.dot(target,u),u.T).reshape(ntargs,nverts,dim)
            
    def compute_combinaison(self,target,rcond = 0.0):
        """
            Computes the combination of base targets allowing to reproduce
            'target' (or giving the best approximation).
            
            arguments :
            - target : target to fit
            - rcond : cut off on the singular values as a fraction of
                      the biggest one. Only base vectors corresponding
                      to singular values bigger than rcond*largest_singular_value
            
        """
        cond = self.s>= rcond*self.s[0]
        u = self.u[ : , cond ]
        vt = self.vt[ cond ]
        s = self.s[cond]
        print target
        return np.dot(np.dot(target.flatten(),u),vt*1./s.reshape(len(s),1))
        
    def compute_combinaison_safe(self,target,rcond = 0.0,regul = None):
        """
            Computes the combination of base targets allowing to reproduce
            'target' (or giving the best approximation), while keeping
            coefficients between 0 and 1.

            arguments :
            - target : target to fit
            - rcond : cut off on the singular values as a fraction of
                      the biggest one. Only base vectors corresponding
                      to singular values bigger than rcond*largest_singular_value
                      
            - regul : regularisation factor for least square fitting. This force
                      the algorithm to use fewer targets.
            
        """
        from cvxmod import optvar,param,norm2,norm1,problem,matrix,minimize
        if type(target) is str or type(target) is unicode :
            target = read_target(target)
        cond = self.s>= rcond*self.s[0]
        u = self.u[ : , cond ]
        vt = self.vt[ cond ]
        s = self.s[cond]
        
        t = target.flatten()
        dim,ntargets = self.vt.shape
        nvert = target.shape[0]
        
        pt = np.dot(u.T,t.reshape(nvert*3,1))
        A = param('A',value = matrix(s.reshape(dim,1)*vt))
        b = param('b',value = matrix(pt))
        x = optvar('x',ntargets)

        if regul is None : prob = problem(minimize(norm2(A*x-b)),[x>=0.,x<=1.])
        else : prob = problem(minimize(norm2(A*x-b) + regul * norm1(x)),[x>=0.,x<=1.])
        
        prob.solve()
        bs = np.array(x.value).flatten()
        # Body setting files have a precision of at most 1.e-3
        return bs*(bs>=1e-3)
        
    
    def combine_targets(self,coefs):
        ntargs,dim,dummy = self.targets.shape
        return (self.targets*coefs.reshape(ntargs,1,1)).sum(0)

def select(choice,subchoice):
    lup = dict([(v,i) for i,v in enumerate(choice)])
    return [lup[c] for c in subchoice]

def find_match(mask,mesh):
    kd = KDTree(mesh)
    return kd.query(mask)

def load_target(filename):
    t = {}
    with open(filename) as f:
        for line in f :
            sp = line.split()
            i = int(sp[0])
            coords = map(float,sp[1:])
            t[i] = coords
    return t

def load_targets(dirname):
    files = os.listdir(dirname)
    files.sort()
    targets = []
    vertices = set()
    for f in files:
        fPath = os.path.join(dirname, f)
        if os.path.isfile(fPath):
            t = load_target(fPath)
            targets.append(t)
            vertices |= set(t.keys())
        
    return [os.path.splitext(f)[1] for f in files],list(vertices),targets

def build_matrix(vert_list,targets):
    look_up = dict([(v,i) for i,v in enumerate(vert_list)])
    base = np.zeros((len(targets),len(vert_list),3))
    for i,t in enumerate(targets):
        for v,coords in t.iteritems() :
            base[i,look_up[v]]=coords
    return base

def fit_mask(head_mesh,head_mask,scan_mesh,scan_mask,base,rcond = 0.0, constrained = False,regul = None):
    if isinstance(base,str):
        base = TargetBase(prefix = base)
    kd_head = KDTree(head_mesh)
    dist,indx = kd_head.query(head_mask)
    head_v = head_mesh[indx]
    
    kd_scan = KDTree(scan_mesh)
    dist,indx = kd_scan.query(scan_mask)
    scan_v = scan_mesh[indx]
    
    target = scan_v - head_v
    if constrained :
        coefs = base.compute_combinaison_safe(target,rcond,regul = regul)
    else :
        coefs = base.compute_combinaison(target,rcond)
    return coefs

def fit_mesh(head_mesh,scan_mesh,base,tofit_verts,init_coefs = None,constrained = False,regul = None,niter = 1):
    if isinstance(tofit_verts,str):
        tofit_verts = np.loadtxt(tofit_verts,'int')
    if isinstance(base,str):
        base = TargetBase(prefix = prefix)
        
    verts = base.vert_list
    ntargs = len(base.targets)

    m = head_mesh.copy()
    nverts = len(scan_mesh)
    
    if init_coefs is not None :
        init_target = base.combine_targets(init_coefs)

    m[verts]+=init_target
    
    kd = KDTree(scan_mesh)
    
    for iter in xrange(niter):
        target = np.zeros((nverts,3))
        dist,indx = kd.query(m[tofit_verts])
        target[tofit_verts] = scan_mesh[indx] - m[tofit_verts]
        target = target[verts]
        if constrained :
            coefs = base.compute_combinaison_safe(target,rcond,regul = regul)
            proj = base.combine_targets(coefs)
        else :
            proj = base.project_target(target)
        if niter > 1 : m[verts]+=(1./niter)*(niter)**(float(iter)/(niter-1)) * proj
        else : m[verts]+= proj

    return m-head_mesh

def save_target(filename,target):
    with open(filename,'w') as f :
        for v,c in target.iteritems():
            if np.abs(c).max()>0 :
                f.write( "%i %s\n"%(v," ".join(["%0.12e"%cc for cc in c]) ) )


if __name__ == '__main__' :
    import wavefront as wf
    import sys
    
    try :
        cmd = sys.argv[1]
    except IndexError :
        print "usage : python scan_fit.py build|project args"
        sys.exit(-1)
    
    if cmd == 'build' :
        try : 
            target_dir = sys.argv[2]
            head_mesh = sys.argv[3]
            head_mask = sys.argv[4]
            output = sys.argv[5]

        except IndexError :
            print "usage : python scan_fit.py build target_dir  head_mesh head_mask output_prefix"
            sys.exit(-1)

        print "Read targets...",
        sys.stdout.flush()
        names,head_verts,targets = load_targets(target_dir)
        print "OK"
        
        print "Build bases...",
        sys.stdout.flush()
        targs = build_matrix(head_verts,targets)
        
        head_mesh = wf.read_obj(head_mesh)
        head_mask = wf.read_obj(head_mask)
        
        kdhead = KDTree(head_mesh.vertices)
        dhead,ihead = kdhead.query(head_mask.vertices)
        
        mask_targets = targs[:,select(head_verts,ihead)]
        mask_base = TargetBase(names,ihead,mask_targets) 
        mask_base.save(output+"_mask")

        base = TargetBase(names,head_verts,targs)
        base.save(output)

    elif cmd == 'fit' :

        try :
            head_mesh = sys.argv[2]
            head_mask = sys.argv[3]
            scan_mesh = sys.argv[4]
            scan_mask = sys.argv[5]
            fit_verts = sys.argv[6]
            prefix = sys.argv[7]
            output = sys.argv[8]
        except IndexError :
            print "usage : python scan_fit.py fit head_mesh head_mask scan_mesh scan_mask fit_verts prefix output_target"
            sys.exit(-1)

        head_mesh = wf.read_obj(head_mesh)
        head_mask = wf.read_obj(head_mask)
        scan_mask = wf.read_obj(scan_mask)
        scan_mesh = wf.read_obj(scan_mesh)

        scan_mesh.vertices,scan_mask.vertices = align_scan(scan_mask.vertices,head_mask.vertices,scan_mesh.vertices)
        scan_mesh.save("aligned.obj")
        
        base_mask = TargetBase(prefix = prefix+"_mask")
        coefs = fit_mask(head_mesh.vertices,head_mask.vertices,scan_mesh.vertices,scan_mask.vertices,base_mask,constrained = True, regul = 0.005)

        base = TargetBase(prefix = prefix)

        target = fit_mesh(head_mesh.vertices,scan_mesh.vertices,base,fit_verts,init_coefs = coefs,niter = 1)

        head_mesh.vertices+=target
        head_mesh.save(output.replace(".target",".obj"))

        save_target(output,dict(zip(base.vert_list,target[base.vert_list])))
    else :
        print "usage : python scan_fit.py build|project args"

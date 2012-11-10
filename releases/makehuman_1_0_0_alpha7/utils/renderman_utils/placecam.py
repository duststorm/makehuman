#Python porting from
#http://graphics.stanford.edu/lab/soft/purgatory/prman/Toolkit/AppNotes/appnote.15.html
#PlaceCamera(): establish a viewpoint, viewing direction and orientation
#for a scene. This routine must be called before RiWorldBegin().
#position: a point giving the camera position
#aim: a point giving the location at which the camera is aimed
#roll: an optional rotation of the camera about its direction axis
#coneangle: an optional spotlight shader cone angle
#

import math
import sys


def usage():
    print "usage: placecam pos_x pos_y pos_z aim_x aim_y aim_z\n"
    print " [coneangle] [roll_angle]\n"
    print " Calculate RenderMan transforms needed for camera transform\n"
    print " from light position to aim point with the given roll angle.\n"

def RiRotate(angle, x, y, z):

    if math.fabs(angle) > 0.001:
        print "Rotate %0.2f %0.2f %0.2f %0.2f\n"% (angle, x, y, z)


def RiTranslate(dx, dy, dz):
    
    print "Translate %0.2f %0.2f %0.2f\n"%(dx, dy, dz)

 
def AimZ(direction): 
    """
    AimZ(): rotate the world so the direction vector points in
    positive z by rotating about the y axis, then x. The cosine
    of each rotation is given by components of the normalized
    direction vector. Before the y rotation the direction vector
    might be in negative z, but not afterward.
    """

    if (direction[0]==0) and (direction[1]==0) and (direction[2]==0):
        return
        
    #The initial rotation about the y axis is given by the projection of
    #the direction vector onto the x,z plane: the x and z components
    #of the direction.
     
    xzlen = math.sqrt(direction[0]*direction[0]+direction[2]*direction[2]);
    if xzlen == 0:
        if direction[1] < 0:
            yrot = 180
        else:
            yrot = 0
    else:
        yrot = 180*math.acos(direction[2]/xzlen)/math.pi;

    #The second rotation, about the x axis, is given by the projection on
    #the y,z plane of the y-rotated direction vector: the original y
    #component, and the rotated x,z vector from above.
    
    yzlen = math.sqrt(direction[1]*direction[1]+xzlen*xzlen);
    xrot = 180*math.acos(xzlen/yzlen)/math.pi; #yzlen should never be 0

    if direction[1] > 0:
        RiRotate(xrot, 1.0, 0.0, 0.0)
    else:
        RiRotate(-xrot, 1.0, 0.0, 0.0)

    #The last rotation declared gets performed first 
    if direction[0] > 0:
        RiRotate(-yrot, 0.0, 1.0, 0.0)
    else:
        RiRotate(yrot, 0.0, 1.0, 0.0)


def PlaceCamera(position, direction, roll):
        RiRotate(-roll, 0.0, 0.0, 1.0);
        AimZ(direction);
        RiTranslate(-position[0], -position[1], -position[2])

def main():

    pos = [0,0,0]
    aim = [0,0,0]
    dir = [0,0,0]
    if len(sys.argv) < 7:
        usage()
        return

    pos[0] = float(sys.argv[1])
    pos[1] = float(sys.argv[2])
    pos[2] = float(sys.argv[3])
    aim[0] = float(sys.argv[4])
    aim[1] = float(sys.argv[5])
    aim[2] = float(sys.argv[6])

    if len(sys.argv) > 7: 
        coneangle = float(sys.argv[7])
    else:
        coneangle = 0.0;

    if len(sys.argv) > 8: 
        roll = float(sys.argv[8])
    else:
        roll = 0.0;

    print "position: %0.2f, %0.2f, %0.2f\n"% (pos[0], pos[1], pos[2])
    print "aim: %0.2f, %0.2f, %0.2f\n"%(aim[0], aim[1], aim[2])
    print "coneangle: %0.4f\n"%(coneangle)
    print "roll: %0.2f\n\n"%(roll);

    if coneangle != 0.0:
        fov = coneangle * 360.0 / math.pi
        print "Projection \"perspective\" \"fov\" [%0.2f]\n"%(fov)


    dir[0] = aim[0] - pos[0]
    dir[1] = aim[1] - pos[1]
    dir[2] = aim[2] - pos[2]

    PlaceCamera(pos, dir, roll)
    return 0
    
if __name__ == "__main__":
    main()


.. _cage:

#######################
Cage and mesh-deform
#######################

If MakeHuman is configured to export a cage and the Cage option is checked during import, the  character comes into Blender with a cage intended for use with the mesh-deform modifier. This  is an alternative method of skinning the mesh, which gives very smooth deformations.   Unfortunately the mesh-deform methods gives too smooth deformation in areas where sharp  creases are intended, which is often the case in the armpits, elbows, knees and groin.   Mesh-deform can be combined with traditional skinning, which perhaps yields the best results.  This is still a very experimental feature, but feel free to explore it if you are adventurous.
 
.. figure::  _static/cage-1.png
   :align:   center
   
   A caged character.

.. figure::  _static/cage-2.png
   :align:   center
   
   Deformation could be better.
 
If the Cage option in the MHX importer was enabled, and the cage mesh was enabled in  the file proxy.fig, things look a little different when the character has been imported.  Apart from the clothes and rig, the character is also surrounded by a low-poly cage.
 
A character using a cage for deformation can not be used out of the box. If we nevertheless  try to pose her as usual, only her arms move. There are now  two modifiers: a mesh-deform modifier above an armature modifier. The armature modifier  is restricted by the vertex group Cage; lower weights mean a smaller influence. Also  note that the multi-modifier option is active. This means that the armature modifier  starts with the mesh state at the top of the stack rather than with the state just  above it.

.. figure::  _static/cage-3.png
   :align:   center
   
   Press Bind to bind the mesh to the cage. }
   
.. figure::  _static/cage-vg.png
   :align:   center
   
   The Cage vertex group.
 
The rest of the deformation should be handled by a mesh-deform modifier, but first  we must bind the mesh to the cage. To do so we simply press the Bind button. Binding  is a rather complex operation which takes several seconds to complete. Other meshes  using mesh-deform, in this case the sweater and the jeans, must also be bound to  the cage.

.. figure::  _static/cage-4.png
   :align:   center
   
   Deformation is still poor.   
   
.. figure::  _static/cage-5.png
   :align:   center

   Character peeks through her cage.

Now the character moves with the rig. Or at least part of the character, because  the deformation is still very poor. The reason is  that the mesh-deform modifier only works if the mesh is entirely enclosed by her  cage; vertices that peek out are not affected by the modifier. The cage was  modelled to entirely cover the default character, but its adaption to other  characters is not perfect.
 
To fix these problems, the cage must be edited in Blender. However, before we  start to edit the cage, all meshes must be unbound from the cage; simply press  the Unbind button that has replaced the Bind button in the mesh-deform modifier.   We now edit the cage, and  once it covers the entire mesh, we bind it to the cage again.
 
Unfortunately, it is still difficult to get a very good deformation with the  MakeHuman mesh. The cage must every surround the mesh, but in the same time  it must not self-intersect. It is difficult to satisfy both these conditions  at the same time, particularly in the groin area, because the left and right   thighs are very close, especially on the jeans. Perhaps one needs to deform the  rest position.

.. figure::  _static/cage-6.png
   :align:   center
    
   Cage edited to cover character entirely.

.. figure::  _static/cage-7.png
   :align:   center
   
   Deformation is better, but not perfect. 

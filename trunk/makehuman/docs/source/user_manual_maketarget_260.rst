
Maketarget for Blender 2.6x 
===========================

1. Open maketarget_b25x.py in Blender's scripting layout. Run the script with Alt-P. A new panel called Make target is created in the UI panel to the right of the viewport. (The UI panel can be toggled on and off with N-key.)

.. image:: _static/1-load.png

2. The panel has two buttons: Load mhclo and load obj. We first press Load obj and navigate to the base mesh.

.. image:: _static/2-obj_loaded.png 

3. After the base mesh has been loaded, two new buttons appear: New target and Load target. Press load target and navigate to a target file.

.. image:: _static/3-target_loaded.png 

4. Target (here young asian female) has been loaded. Several new buttons appear.

5. Edit the target in some way. Tab toggles in and out of edit mode, O-key toggles proportional editing on and off.

.. image:: _static/4-target_edited.png

6. Symm Left -> Right, and then Save target. Overwriting the old target requires confirmation.

.. image:: _static/5-after_symm_left2right.png  

7. Discard the target and import the mhclo version of the base mesh instead. This of course requires that the mhclo file has been created. How to do that is described here. Also, the Self-clothed option must be selected. Since the process is quite fragile it might be best if I do it. To that end one needs the new base.obj with extra geometry added.

.. image:: _static/7-mhclo_loaded.png

8. Assuming that the mhclo file exists and has been loaded, we can then load a target like before.

.. image:: _static/8-child_target_loaded.png 

9. Press fit target.

.. image:: _static/9-target_fitted.png 

10. Edit and save target.

11. Load a target which only affects part of the body. The affected verts are selected when the target has been loaded.

.. image:: _static/10-partial_target_loaded.png  

12. fit target. The affected clothing verts have also been selected. Save the target with SelectedOnly = 1.
 
.. image:: _static/11-partial_target_fitted.png

.. _faq:

###########################
Frequently asked questions
###########################

**********************
Textures
**********************

A0:
    Where should we put the custom textures, on order to see them in MH library?
    
A0:
    Documents\\makehuman\\data\\skins on windows, ~\\makehuman\\data\\skins on linux. You can see that if you open the skins library and look left down, the path is written there.

**********************
Save/export questions
**********************

Q0: 
    Where are saved and export the files, when I press the "save" or export "buttons"?

A0: 
    In general this depends on the system you run MakeHuman.

    * For Windows and Linux: When you start the software, a new folder, called "makehuman" is created in your home directory. All your saved makehuman files are saved into makehuman/models and all your exported files are into makehuman/exports.

    * For Mac OS-X: All Documents which are created are stored within the users Documents folder. MakeHuman will create a subfolder named 'HakeHuman' herein. This contains another three subfolders: 'models', 'exports' and 'renderman'.
 
Q1: 
    Where is my home directory?

A1: 
    Assuming you are the user named "Foo", you have installed Windowson a C:/ drive and you are working in Windows 2000 or XP, your home directory is: C:\Documents and Settings\Foo

****************
Legal questions
****************

Q0: 
    Briefly, what can I do with the exported makehuman character?

A0: 
    You can do all you want, except use it to make a MakeHuman-like differently licensed (i.e. closed source or closed source suitable, LGPL licensed for example) software.  All other questions below are about details around this concept.

Q1: 
    Where can I read the official license of makehuman?

A1: 
    Here (to do: link)
    
Q2: 
    Can I use makehuman output models for commercial purposes?

A2: 
    Yes, but not if the commercial purpose is a closed source clone (or something similar, closed source suitable). The specific data files used to define and deform the mesh, distributed with the MakeHuman application are covered by the terms of the GNU General Public License 3.0 and you are granted permission to use and redistribute those files in original or modified form under those terms. 
    
    These data files can also be manipulated using the Blender MakeTarget script, but they, and derivative works remain under the terms of the GNU GPL. When you export, save, or in any way convert a MakeHuman data file, you may store any deformations that you have applied/created, along with the topology of the base mesh and any positional information that you have not materially changed. 
    
    You are the Copyright holder of changes that you have made. The MakeHuman Team retains Copyright over the topology and the base mesh, but grants you permission to copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the generated materials over which they hold Copyright, including the topology and positional information constituting the base mesh provided that this does not prevent others from doing the same.
 
Q3: 
    I want to to use MakeHuman targets data and MakeHuman mesh in a differently licensed makehuman-like. Because I can sublicense the output mesh, I'll do this: I'll apply a target in makehuman, then I'll export the mesh (so I'm the copyright holder of it), and as last step, I'll extract the target from it (so I'm the copyright holder of the morph too). It's legal, isn't it?

A3: 
    No, you can't. Because you are the copyright holder only of changes you have made (if you made them, in example retouching the mesh manually in Blender, doing things impossible to model using just the makehuman data), as specified here. So you are using material under MakeHuman (c), and we can act legally against you.

Q4: 
    That would mean that people who only use pure MH targets don't have a model that belongs to them?

A4: 
    They never have an model that 100% belong to them. But this shouldn't worry them, as our model licence permit them, anyway to copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the models. The percentage of copyright we retain is just an insurance for us in case of illegal use (MH differently licensed clone or similar cases), and should worry only people that want to do a massive extractions  of targets data from MakeHuman.

Q5: 
    "And/or sell copies", so selling can be without sublicense, no?
    
A5: 
    It can be without sublicense, but, of course, not without the Original License. Our users can include Original License, or add a Sublicense (that mean Original license + Custom Additional License). Anyway note that Original License is so permissive that's practically "invisible" from users point of view, except the case they are selling hundreds meshes to make a MakeHuman differently licensed clone...

Q6: 
    Why does the MakeHuman team retain a partial Copyright on the output models?

A6: 
    We need to protect the hard work done to model the base mesh and all morphs. The Copyright will be used in case someone tries to use our efforts in a closed source clone or differently licensed clone.

Q7: 
    Why you don't you use the GPL for the output models too?

A7: 
    When our output was GPLed, a lot of artists complained about the obligation to release a public GPLed version of their works. Most of our users need to include their creations in commercials works, for example games, movies, etc. They shouldn't be forced to release their personal creations under the GPL (you know, the GPL is an auto-propagating license). So, with our solution, decided after a very long discussion, our users are free to do all they want, except to use the MH output in an MH differently licensed clone.

Q8: 
    Why don't you use the LGPL for the makehuman data?

A8: 
    Because the biggest part of the MakeHuman software (years of artistic 3d modeling) IS the data. Releasing the data under the LGPL is more likely to release the whole software under LGPL. This would permit the birth of a differently licensed clone that uses our effort for their business, or to see our work used by closed source competitors. LGPL works for libraries, not for complete software.

Q9: 
    I plan to create a differently licensed library with the same functionality as makehuman, using the MakeHuman data. Can I do it?

A9: 
    No. If you write routines that mimic makehuman, you need to use the target data, which is under the GPLv3 like the code. This is because the target data is part of our routines to model a human procedurally. We need to protect the hard work that went in it. If you want a non-GPLv3 version of the routines, you will have to remodel all targets by yourself, as they are copyrighted under the GPLv3.

Q10: 
    Does 'target files' include the human mesh itself?

A10: 
    No. They just include the difference vectors from a part of human mesh before and after modelling.
    
Q11: 
    Can I use MakeHuman characters for a closed source game to sell?

A11: 
    Yes, of course,  if the "game" is not a MakeHuman clone or similar.

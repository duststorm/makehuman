.. _basemesh:

.. highlight:: python
   :linenothreshold: 5


Evolution Towards a Universal Model topology: the HoMunculus
=============================================================

The principal aim of the MakeHuman project is to develop an Open Source application capable of realistically modelling a very wide variety of human anatomical forms in the full range of natural human poses from a single, universal mesh.

Central to this is the design of a 3D humanoid mesh that can readily be parametrically manipulated and deformed to represent alternative anatomical characteristics while retaining and respecting a common structural skeleton that permits poses and the corresponding deformations to also be parametrically manipulated. 

This objective has been pursued to afford the artist the maximum degree of experimental freedom when using the software. It frees the artist from the artificial constraints that are inherent to a model that has pre-established gender or age.

.. figure::  _static/three_ribs.png
   :align:   center
   
   Evolution of the ribs topology.

By pursuing this aim the MakeHuman Team have developed a model that can combine different anatomical parameters to transition smoothly from the infant to the elderly, from man to woman and from fat to slim. The vast wealth of potential combinations provides the artist with an extraordinarily broad range of possibilities for artistic expression but presents many interesting problems to the development team. 


.. figure::  _static/hm01.png
   :align:   center
   
   The first official base mesh (2002). No male, no female, nor young or old. A perfect neutral body.



In particular it adds to the classical problems of 3D modelling (number of polygons, square or triangular faces, etc.) the problems of constructing a super mesh that can be transformed into any form of human while being sufficiently optimised to be able to be manipulated on desktop machines, yet still producing a professional quality of output. 

These discussions resulted in agreement that the initial mesh should occupy a middle ground, being neither pronounced masculine, nor pronounced feminine, neither young nor old and having a medium muscular definition. An androgynous form, the HoMunculus. A form midway between male and female, old and young, thin and fat, muscular and lean.

.. figure::  _static/three_hands.png
   :align:   center
   
   Evolution of the hand topology.

The current MakeHuman mesh has evolved through successive iterations of the MakeHuman project, incorporating lessons learned, community feedback and the results of considerable amounts of study and experimentation. No generic mesh is perfect and this mesh has inevitably been subject to some compromise and will undoubtedly continue to be refined in future releases. Nevertheless, the current mesh represents a remarkable achievement and is a great source of pride for the MakeHuman team. The current iteration, known as the 'HM06' comprises a state of the art universal humanoid model. This paper describes the characteristics and capabilities of the mesh along with a brief history and discussions about potential future enhancements.


.. figure::  _static/head_story.png
   :align:   center
   
   Evolution of the head topology.
   
Since the first release of MH (2000) and the first release of makeHead(1999), the challenge was to construct a universal topology that retained all of these capabilities but added the ability to interactively, programmatically adjust the mesh to accommodate the variety of anatomical variety found in the human population. This challenge could have been addressed by dramatically increasing the number of vertices used for the mesh, but the resultant, dense mesh would have limited the performance on all but top end machines and, even with extremely powerful computers it is generally recognised that an optimised mesh is preferable to one containing useless or morphologically insignificant points because:

* A more economic number of control points supports more orderly and precise modelling, avoiding the confusion of edges inherent to a more dense model
* The savings on processor and memory resource can be better invested in providing more sophisticated functionality and greater fluidity to the artist
* The lighter model better supports the possibility of incorporating larger numbers of characters into a rendered scene

So, the model developed for MH is:

* Light and optimized for subdivision surfaces modelling (14638 verts, including teeth).
* Quads only. The human mesh is completely triangles free.
* Optimized for animation, including all loops used by high level artists.

The evolution of the mesh through successive iterations illustrates a number of interesting concepts that have been explored and the understanding that has been encapsulated into the current mesh.

.. figure::  _static/kmesh.png
   :align:   center
   
   Some differences between HM01 and HM02.
   
* The first prototype of an universal mesh (head only) was done in 1999 in the makeHead script, and then adapted for the early MH (2000),
* The first professional model, HM01, was realized by Enrico Valenza in 2002.
* The second remarkable mesh (K-Mesh or HM02) was modelled by Kaushik Pal in 2005
* The third mesh was modelled by Manuel Bastioni upon the (z-mesh or HM03);
* The fourth mesh was modelled by Gianluca Miragoli (aka Yashugan) in 2007 and builds upon the experience gained on the preceding versions (Y-Mesh or HM04)
* The fifth mesh build upon the previous one by Gianluca Miragoli and Manuel Bastioni (HM05)
* The sixth mesh build upon the previous one by Gianluca Miragoli.
* Latest mesh, released in 2010, is actually the state of the art (artists: Waldemar Perez Jr., André Richard, Manuel Bastioni).

The knowledge gained over the years has driven the simplification and optimization of the model. A highly sophisticated and detailed model can be good for static, one-off models, but an application designed for real-time manipulation of related groups of parameters and for real-time visualisation needs to be efficient. The MakeHuman solution to these contradictory pressures is to create a simplified, optimized model and to support the generation of sub-surfaces that can be used to smooth out imperfections before rendering. 

.. figure::  _static/tav2.png
   :align:   center
   
   Some topology improvements in HM06

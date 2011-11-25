.. _plugin_system:

.. highlight:: python
   :linenothreshold: 5

************************
Makehuman plugin system
************************

.. _plugins:

Plugins
=========


Makehuman has a simple plugin framework which makes it easy to add and remove features. At startup, MakeHuman now looks for .py files in the plugins folder which are not starting with an underscore (which makes it easier to disable unwanted plugins).

It loads them one by one and calls the load entry point passing a reference to the application. The plugin can use this reference to add the necessary GUI widgets or code to the application.

The rules for plugins are very simple:

* A plugin is a .py file in the plugins folder with a load entry point.
* A plugin only imports core files.

The reason a plugin cannot import other plugins is that it would make it difficult to know which files belong to which plugin. We still need to define a convention for shared files beyond the core MakeHuman files. To get started look at example.py or any of the other plugins to see how you can create your own feature in MakeHuman.

GUI
====

The GUI in MakeHuman is still far from finished. Since the first alpha there have been many changes already and many other will come. This is because when features are added or modified, we can run out of space, or start to see things differently. 

Some times we experiment to see how a modifier can be manipulated in a different way. For example in the details and microdetails we chose to have tools manipulating the model
directly instead of using sliders. A

nother idea for the macrodetails was a multidimensional slider, like a radar chart which would replace all five sliders. It is impossible to pour the GUI into into its final form while we are still adding functionality and getting new ideas. However don’t let the lack of guidelines stop you from adding a GUI to your own plugins. 

The current GUI API is very usable, and gets more mature every day. The layout at the moment is a two level tab control. The tabs at the top represent categories, like modeling, files, rendering. The ones at the bottom are the tasks in the current category and refine the more broad category in macrodetail, detail and microdetail modeling, or saving, loading and exporting. 

So when creating your plugin, the first thought should be "In which category does it belong?". From experience we know that it can be a though question to answer. Sometimes the only answer is adding a new category. This is what we initially did for measurement for example

::

    def load(app):
        category = gui3d.Category(app, "Measurement")

Next you probably want your own task to implement your feature. While it’s possible to attach functionality to an instance of gui3d.Task, it’s often easier to derive your own class. 

When you create an instance of your class, you pass the parent of your task, which can either be an existing category

::

    def load(app):
        taskview = HairPropertiesTaskView(app.categories["Modelling"])

or the new one which you added.

::

    def load(app):
        category = gui3d.Category(app, "Measurement")
        taskview = MeasurementTaskView(category)


In your derived task you will then add the necessary controls to let the user interact.
A good place to see how to use the different controls is the example plugin. You will see that even if you don’t add any controls, the model is already visible. This is because the model is attached to the root of the GUI tree. 

In the onShow event of your task you might want to reset the camera position, like we do in the save task, or hide the model, like we do in the load task. Just don’t forget to reset the state when your task gets hidden in onHide.

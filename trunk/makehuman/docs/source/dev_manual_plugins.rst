.. _writing_plugins:

.. highlight:: python
   :linenothreshold: 5

***************
Writing plugins
***************

.. _plugins:

Plugins
=========


Makehuman has a simple plugin framework which makes it easy to add and remove
features. At startup, MakeHuman now looks for .py files in the plugins folder which are
not starting with an underscore (which makes it easier to disable unwanted plugins).
It loads them one by one and calls the load entry point passing a reference to the
application. The plugin can use this reference to add the necessary GUI widgets or
code to the application.
The rules for plugins are very simple:

* A plugin is a .py file in the plugins folder with a load entry point.
* A plugin only imports core files.

The reason a plugin cannot import other plugins is that it would make it difficult to
know which files belong to which plugin. We still need to define a convention for
shared files beyond the core MakeHuman files. To get started look at example.py or
any of the other plugins to see how you can create your own feature in MakeHuman.

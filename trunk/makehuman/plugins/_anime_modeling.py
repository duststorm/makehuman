#!/usr/bin/python
# -*- coding: utf-8 -*-
import gui3d


class AnimeModelingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Anime modelling', category.app.getThemeResource('images', 'macro.png'))


taskview = None


def load(app):
    taskview = AnimeModelingTaskView(app.categories['Modelling'])

def unload(app):
    pass

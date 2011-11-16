
.. highlight:: python
   :linenothreshold: 5

.. _undoredo:

Undo-redo
=========


One of the first features written was undoredo. Having this from the start saves us
a lot of time later as we add this functionality to each kind of model modification
immediately. It is important that every modification is undoable, since just one undo
able modification would leave the user without the possibility to undo anything. So it’s
crucial that if you write a plugin which modifies the model, you also make undo work.
The Application class has several methods to work with actions. An action is a class
with two methods, do and undo. If the action itself does the modification you can use
app.do to add it to the undo stack. If you did the modification yourself already during
user interaction, you can add the action using app.did. The application won’t call the
do method of the action in that case. If you want to make your own undoredo buttons,
you can use app.undo and app.redo. To illustrate, here is the action we use to change
the hair color:

::

    class Action:
        def __init__(self, human, before, after, postAction = None):
            self.name = "Change hair color"
            self.human = human
            self.before = before
            self.after = after
            self.postAction = postAction

        def do(self):
            self.human.hairColor = self.after
            if self.postAction:
                self.postAction()
            return True

        def undo(self):
            self.human.hairColor = self.before
            if self.postAction:
                self.postAction()
            return True

The postAction is a handy way to specify a method to keep your GUI in sync with
the changes. In this case we update the color control to show the correct color when
the user chooses to undo or redo the hair color change.

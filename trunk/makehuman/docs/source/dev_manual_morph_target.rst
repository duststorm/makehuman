
.. highlight:: python
   :linenothreshold: 5

.. _morph_targets:

Morph targets
==============

Whatever your plugin does, there’s a big chance that it will modify the model. As
many of you probably know, MakeHuman doesn’t work mathematically or procedural,
but artistically. This means that you don’t just drag vertices when moving a part
of the body, but you actually apply a morph made by an artist. There are different
kind of morphs targets which are applied in different ways. Macro targets, which
are the most complex internally, are ironically the easiest to use: human.setGender,
human.setAge, human.setWeight and human.setMuscle can be used to change the cor
responding macro features. Height was originally not there, so you had to make the
modifier yourself. We will look at that in a moment. Detail and micro detail targets
both come in pairs. For example one target to move a body part to the left, and another
target to move the same body part to the right. Therefore you should never apply both
targets at the same time. This means that when you apply one, and later you want to
apply the other, you need to remove the first. While you could use human.setDetail to
this, it is easier to use the Modifier class which does all of the needed logic behind the
the method modifier.setValue, it has an accompanying modifier.getValue which has the
reverse logic. To use it, you create a modifier passing the two opposite targets:

::

    modifier = humanmodifier.Modifier(
        "data/targets/macrodetails/universalstaturedwarf.target",
        "data/targets/macrodetails/universalstaturegiant.target")
    modifier.setValue(human, 0.0)

A value between 1.0 and 0.0 will use the dwarf target, while a value between 0.0
and 1.0 will use the giant target. Using 0.0 will remove both targets. While using a
modifier also applies the target, to keep changes interactive other targets are not reapplied
and normals are not recalculated. Once you have made the necessary changes,
you commit them using human.applyAllTargets. Which does exactly what it says. It
applies all the targets one by one and additionally recalculates the normals. Reapplying
all targets minimizes the size of mathematical error in the final model.

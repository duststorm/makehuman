
.. highlight:: python
   :linenothreshold: 5
 

.. _Asynchronous:

Asynchronous calls and animation
================================

When doing lengthy operations it is important not to block the GUI from redrawing.
Since everything runs in one thread, it is easy to block the event loop in your plugin.
There are 4 ways to avoid this, depending on the need.
If no user interaction is needed, a progressbar can be used. A progressbar uses
the redrawNow() method of the application. This redraws the screen outside the event
loop. Instead of creating your own progressbar, it is advised to use the progress method,
which uses the global progressbar. Calling progress with a value greater than zero
shows the progressbar, a value of zero hides it.

::

    inc = 1.0 / n
    value = inc
    for i in xrange(n):
        # Shows the progressbar the first time
        self.app.progress(value)
        ...
        value += inc
    # Hides the progressbar
    self.app.progress(0)

If user interaction is desired during the operation, either asynchronous calls, a timer
or a thread can be used.
Asynchronous calls are used when a lengthy operation can be split in several units.
It is used for example in the startup procedure as well as for the plugin loading loop.
The mh.callAsync(method) queues the calling of method in the event loop, so it will
be called when the event gets processed. In case different methods need to be called
after each other, as in the startup procedure, callAsync is used to call the next method.

::

    def method1(self):
        ...
        mh.callAsync(self.method2)

In case of the plugin loading loop, it calls the same method until it is done.

::

    def method(self):
        if continue :
            mh.callAsync(self.method)


This is not to be used for animations, as it takes very little time between calling
callAsync and the event loop calling the method. Calling time.sleep(dt) to avoid this
should not be done as it blocks the main thread. For animations use timers instead. An
example of this can be found in the BvhPlayer plugin. The method mh.addTimer(interval,
method) adds a timer which calls the given method every interval milliseconds.
It returns a value to be used by removeTimer to stop the timer.

::

    def play(self):
        self.timer = mh.addTimer(33, self.nextFrame)

    def pause(self):
        mh.removeTimer(self.timer)

    def nextframe(self):
        ...

If a lengthy operation includes blocking on sockets or pipes, it is advised to use a
python thread. However this has been shown to be problematic on Linux. To get around the problems
on linux you should not access any makehuman structures from within your thread,
but use mh.callAsync to call the methods from the main thread. See the clock
plugin example for example code on how to use threads correctly.



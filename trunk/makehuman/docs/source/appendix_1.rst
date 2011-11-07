.. _appendix_1:

.. highlight:: python
   :linenothreshold: 5

*********************************************
Appendix 1 -Rst sintax-
*********************************************

.. _plugins:

Using math
===========

All math formulas, expression etc, can be included in Sphinx using the *math* directive. The general sintax is::

    .. math::

       [your math here]


Subscripts and superscripts
---------------------------

::

       \alpha_i > \beta_i

.. math::

   \alpha_i > \beta_i

::

        \sum_{i=0}^\infty x_i

.. math::

    \sum_{i=0}^\infty x_i


Fractions, binomials and stacked numbers
-----------------------------------------

::

    \frac{3}{4} \binom{3}{4} \stackrel{3}{4}    

.. math::

    \frac{3}{4} \binom{3}{4} \stackrel{3}{4}
    
::

    \frac{5 - \frac{1}{x}}{4}

.. math::

    \frac{5 - \frac{1}{x}}{4}

::

    (\frac{5 - \frac{1}{x}}{4})

.. math::

    (\frac{5 - \frac{1}{x}}{4})

::

    \left(\frac{5 - \frac{1}{x}}{4}\right)

.. math::

    \left(\frac{5 - \frac{1}{x}}{4}\right)

Radicals
--------

::

    \sqrt{2}

.. math ::

    \sqrt{2}
    
::

    \sqrt[3]{x}

.. math::

    \sqrt[3]{x}


Symbols
-------

fooo fooo fooo :math:'\alpha > \beta' fooo
























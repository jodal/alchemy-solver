Alchemy Solver
==============

This is a game solver for the Alchemy game found in the Chrome Web Store or at
http://alchemy.l8r.pl/. Using this program is called cheating, though it was
fun to make the solver.


Usage
-----

The program requires Python, python-lxml, and python-pygraphviz to run.

To list all known elements::

    python alchemy_solver.py --list

To create a PNG file showing the complete solution of the game::

    python alchemy_solver.py --game

To create a PNG file showing the full solution of a single element, e.g.
``isle``::

    python alchemy_solver.py --full isle

To create a PNG file showing all the elements that can be made from a single
element, e.g. ``water``, in one step::

    python alchemy_solver.py --from water

To create a PNG file showing just the last step of construction of a single
element, e.g. ``steam``::

    python alchemy_solver.py --to steam

The three last commands will create solutions for all elements if given the
argument ``all`` instead of an element name.

Generated PNG files will be placed in the ``solutions/`` directory.


License
-------

The source code is copyright Stein Magnus Jodal and licensed under the Apache
License, Version 2.0.

The XML files are taken from the game. They can be found at
http://alchemy.l8r.pl/library.xml and http://alchemy.l8r.pl/en_us.xml.

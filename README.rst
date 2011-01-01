Alchemy Solver
==============

This is a game solver for the Alchemy game found in the Chrome Web Store or at
http://alchemy.l8r.pl/. Using this program is called cheating, though it was
fun to make the solver.


Usage
-----

The program requires Python, python-lxml, and python-pygraphviz to run.

To create a PNG file showing the complete solution of the game::

    python alchemy-solver.py --full

To create a PNG file showing the solution of a single element, provide the
element name, e.g. ``isle``::

    python alchemy-solver.py isle

To create PNG files for both the full solution and all elements::

    python alchemy-solver.py --all


License
-------

The source code is copyright Stein Magnus Jodal and licensed under the Apache
License, Version 2.0.

The XML files are taken from the game. They can be found at
http://alchemy.l8r.pl/library.xml and http://alchemy.l8r.pl/en_us.xml.

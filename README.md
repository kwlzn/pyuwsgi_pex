pyuwsgi_pex
===========

a python wrapper around pex-bootstrapped uWSGI


Build/Deploy Instructions
=========================

 1) uprev the right-most minor version in setup.py (the rest maps to the uwsgi version,
    e.g. '2.0.6.0' is uwsgi 2.0.6 release 0; '2.0.6.1' is uwsgi 2.0.6 release 1, etc)

 2) make the 'build_pydist' target and set your target python interpreter (defaults to 2.7):

    $ make build_pydist PYTHON=python2.6

 3) rename the egg to a platform specific name, e.g.

     $ mv -f pyuwsgi_pex-2.0.6.0-py2.6{,-linux-x86_64}.egg

 4) add the egg to your distribution server

 5) repeat for all permutations of python versions and platforms

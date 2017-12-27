
.. image:: https://secure.travis-ci.org/ravihuang/robotframework-stublibrary.png?branch=master
  :target: http://travis-ci.org/ravihuang/robotframework-stublibrary

robotframework-stublibrary
--------------------------

**robotframework-stublibrary** is a `Robot Framework
<http://code.google.com/p/robotframework/>`_ test library for all your HTTP
needs. It uses `webtest <http://webtest.pythonpaste.org/>`_ library
underneath now.

Installation
------------

You can install robotframework-stublibrary via `pip
<http://www.pip-installer.org/>`_::

  pip install --upgrade robotframework-stublibrary

Usage
-----
API documentation can be found at
`https://github.com/ravihuang/robotframework-stublibrary
<https://github.com/ravihuang/robotframework-stublibrary/>`_, here is an example
on how to use it:

============  ================
  Setting          Value      
============  ================
Library       StubLibrary
============  ================

\

============  =================================  ===================================
 Test Case    Action                             Argument
============  =================================  ===================================
Example

============  =================================  ===================================


Compatibility
-------------
This library is only tested on CPython. It might work on Jython, not sure.

Development
-----------
If you want to hack on this library itself, this should get you started::

  # install
  git clone https://github.com/peritus/robotframework-stublibrary.git
  cd robotframework-stublibrary/
  python setup.py install
    
  # run tests
  pybot tests/

I'm very happy about patches, pull-requests and API-discussions (as this is
mostly a wrapper supposed to have a nice API)!

Changelog
---------

**v0.1.0**

- new

License
-------
Apache License


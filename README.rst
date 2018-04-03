robotframework-stublibrary
==========================
.. image:: https://secure.travis-ci.org/ravihuang/robotframework-stublibrary.png?branch=master
  :target: http://travis-ci.org/ravihuang/robotframework-stublibrary

Introduction
------------
robotframework-stublibrary is a `Robot Framework <https://pypi.python.org/pypi/robotframework>`_ test library for all your HTTP
needs. It uses:
`webtest <http://webtest.pythonpaste.org/>`_ 
`gevent <https://pypi.python.org/pypi/gevent>`_ 
`falcon <https://pypi.python.org/pypi/falcon>`_ 
`py_fake_server <https://github.com/Telichkin/py_fake_server>`_ 
library underneath now.

Installation
------------

You can install robotframework-stublibrary via `pip <http://www.pip-installer.org/>`_::

  pip install --upgrade robotframework-stublibrary

Usage
-----
here is an example on how to use it:
`https://github.com/ravihuang/robotframework-stublibrary/blob/master/tests/tests.txt
<https://github.com/ravihuang/robotframework-stublibrary/blob/master/tests/tests.txt>`_, 

============  ================
  Setting          Value      
============  ================
Library       StubLibrary
============  ================

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

**v0.1.3**

- new

License
-------
Apache License


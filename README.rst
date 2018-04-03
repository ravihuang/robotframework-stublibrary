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
Case-01
    log    1.create server
    ${x}    Create Server    http://0.0.0.0:8123
    Add Response    get    /hello    body=Hello, 8123
    ${y}    Create Server    http://0.0.0.0:4567
    Add Response    get    /hello    body=Hello, 4567
    log    2.switch server
    Switch Server    ${x}
    Add Response    get    /things    body=------8123
    Switch Server    ${y}
    Add Response    get    /things    body=------4567
    log    3.create session
    Create Session    a    http://127.0.0.1:8123
    Create Session    b    http://127.0.0.1:4567
    log    4.get
    ${resp}    Get Request    a    /hello
    Should Be Equal    ${resp.text}    Hello, 8123
    ${resp}    Get Request    a    /things
    Should Be Equal    ${resp.text}    ------8123
    log    5,check1
    Switch Server    ${x}
    Should Call 1 Time    get    /hello
    Should Call x Time    get    /things    0    svr=${y}
    ${resp}    Get Request    b    /hello
    Should Be Equal    ${resp.text}    Hello, 4567
    ${resp}    Get Request    b    /things
    Should Be Equal    ${resp.text}    ------4567
    log    6,check2
    Should Call x Time    get    /hello    1    svr=${y}
    Should Call x Time    get    /things    1    svr=${y}
    Close All Server
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

**v0.1.3**

- new

License
-------
Apache License


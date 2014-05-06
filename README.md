buzzword-ipsum
==============

Requirements
===
* Python 2.7
* pip
* node
* npm

Development
===

To develop with the built-in webserver serving the webapp and the static
files:

    cd webapp
    python setup.py develop
    cd buzzwordipsum
    python webservice.py

This will also auto-refresh Python and static file changes.

Go to http://localhost:5000/index.html ('/' will not work because the development mode doesn't have directory indexes).

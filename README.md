buzzword-ipsum
==============

Setup (still to be automated/made easier):

Install python 2.7, node, npm, pip, virtualenv, virtualenvwrapper
Set $WORKON_HOME and source virtualenvwrapper shell script

Set up virtualenv and install required python packages
$ mkvirtualenv buzzwordipsum
$ workon buzzwordipsum
$ pip install Flask Flask-RESTful coverage nose
$ pip install Pattern --allow-external Pattern --allow-unverified Pattern
$ deactivate

Install grunt stuff in the local directory:
$ npm install

Run linting and tests:
$ grunt check

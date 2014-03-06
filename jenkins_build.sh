#!/bin/bash
export WORKON_HOME=/usr/local/virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon buzzwordipsum
npm install
grunt deploy --wsgiTarget=$WSGI_TARGET --staticTarget=$STATIC_TARGET

#!/bin/bash

export WORKON_HOME=/usr/local/virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon $VENV_NAME
npm install
cd webapp && python setup.py develop
grunt deploy --wsgiTarget=$WSGI_TARGET --staticTarget=$STATIC_TARGET

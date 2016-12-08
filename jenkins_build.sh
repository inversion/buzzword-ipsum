#!/bin/bash

set -o xtrace

export WORKON_HOME=/usr/local/virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon $VENV_NAME
set -o errexit
yarn install
cd webapp && python setup.py develop
grunt deploy --wsgiTarget=$WSGI_TARGET --staticTarget=$STATIC_TARGET

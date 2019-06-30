#!/usr/bin/env bash

. ci/ci-functions.sh

echob "generating message api..."
citest pip install jinja2
citest generate/generate-python.py --output-dir=brping

echob "testing message api..."
citest python brping/pingmessage.py

echob "installing package..."
citest python setup.py install

echob "update gh pages..."
citest pip install pyOpenSSL
citest ci/update-gh-pages.sh

echob "deploying..."
citest ci/deploy.sh

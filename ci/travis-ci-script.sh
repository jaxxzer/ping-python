#!/usr/bin/env bash

. ci/ci-functions.sh

echob "Generating Message APi."
citest pip install jinja2 && generate/generate-python.py --output-dir=brping

echob "Testing message api."
citest python brping/pingmessage.py

echob "installing package..."
citest python setup.py install

echob "update gh pages..."
citest pip install pyOpenSSL && ci/update-gh-pages.sh

citest false

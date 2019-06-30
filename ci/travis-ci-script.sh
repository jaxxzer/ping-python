#!/usr/bin/env bash

. ci/functions.sh

echob "generating message api..."
pip install jinja2 && generate/generate-python.py --output-dir=brping || exit 1

echob "testing message api..."
python brping/pingmessage.py || exit 1

echob "installing package..."
python setup.py install || exit 1

echob "update gh pages..."
pip install pyOpenSSL && ci/update-gh-pages.sh || exit 1

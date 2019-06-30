#!/usr/bin/env bash

. ci/ci-functions.sh

echob "Generating Message APi."
citest pip install jinja2 && generate/generate-python.py --output-dir=brping

echob "Testing message api."
python brping/pingmessage.py || exit 1

echob "installing package..."
python setup.py install || exit 1

echob "update gh pages..."
pip install pyOpenSSL && ci/update-gh-pages.sh || exit 1

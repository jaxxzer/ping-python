#!/usr/bin/env bash

python setup.py install --user || exit 1
python brping/pingmessage.py || exit 1
ci/test-ci.py || { pip install pyOpenSSL --user && ci/test-ci.py; } || exit 1
ci/update-gh-pages.sh || exit 1

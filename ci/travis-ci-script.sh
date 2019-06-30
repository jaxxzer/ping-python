#!/usr/bin/env bash

echo "installing lib..."
python setup.py install || exit 1

echo "testing message api..."
python brping/pingmessage.py || exit 1

echo "update gh pages..."
pip install pyOpenSSL && ci/update-gh-pages.sh || exit 1

#!/usr/bin/env bash

. ci/ci-functions.sh

citest git checkout deployment
citest git reset
citest cat ci/deploy-whitelist | xargs git add
citest git status
citest git commit -m "automated deployment"

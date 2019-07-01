#!/usr/bin/env bash

. ci/ci-functions.sh

test git branch -a
test git branch
test cat ci/deploy-whitelist
test cat ci/deploy-whitelist | xargs git add -f
test git commit -m temporary-commit
test git checkout deployment
test git checkout HEAD@{1}
test git diff --staged
test git commmit -m "update auotgenerated files"
test git log
test git show

#!/usr/bin/env bash

. ci/ci-functions.sh

test git config remote.origin.fetch +refs/heads/*:refs/remotes/origin/*
test git fetch origin deployment
test git branch -a
test git branch
test cat ci/deploy-whitelist
cat ci/deploy-whitelist | xargs git add -f
git commit -m temporary-commit
test git checkout deployment
test git checkout HEAD@{1} ci/deploy-whitelist
cat ci/deploy-whitelist | xargs git checkout HEAD@{1}
test git --no-pager diff --staged
test git commit -m "update auotgenerated files"
test git --no-pager log
test git --no-pager show

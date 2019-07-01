#!/usr/bin/env bash

bold=$(tput bold)
normal=$(tput sgr0)
testN=0

echob() {
    echo "${bold}${@}${normal}"
}

test() {
    echob "$@"
    echo "travis_fold:start:$testN"
    "$@"
    echo "travis_fold:start:$testN"
    testN=$(($testN+1))
    echo $testN
    exitcode=$?
    echob "$@ exited with $exitcode"
    if [ $exitcode -ne 0 ]; then exit $exitcode; fi
}

#!/usr/bin/env bash

bold=$(tput bold)
normal=$(tput sgr0)
testN=0

echob() {
    echo "${bold}${@}${normal}"
}

test() {
    echob "$@"
    echo -en 'travis_fold:start:#{testN}\\r'
    "$@"
    echo -en 'travis_fold:start:#{testN}\\r'
    $testN=$testN + 1
    exitcode=$?
    echob "$@ exited with $exitcode"
    if [ $exitcode -ne 0 ]; then exit $exitcode; fi
}

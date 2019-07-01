#!/usr/bin/env bash

bold=$(tput bold)
normal=$(tput sgr0)

echob() {
    echo "${bold}${@}${normal}"
}

test() {
    echob "$@"
    "$@"
    exitcode=$?
    echob "$@ exited with $exitcode"
    if [ $exitcode -ne 0 ]; then exit $exitcode; fi
}

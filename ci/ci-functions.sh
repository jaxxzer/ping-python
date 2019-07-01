#!/usr/bin/env bash

bold=$(tput bold)
normal=$(tput sgr0)

echob() {
    echo "${bold}${@}${normal}"
}

test() {
    echob "$@"
    "$@"
    result=$?
    echob "$@ exited with $result"
    if [ $result -ne 0 ]; then exit $result; fi
}

#!/usr/bin/env bash

bold=$(tput bold)
normal=$(tput sgr0)

echob() {
    echo "${bold}${@}${normal}"
}

test() {
    echob "$@"
    $@ || exit 1
}

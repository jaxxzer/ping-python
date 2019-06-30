#!/usr/bin/env bash

bold=$(tput bold)
normal=$(tput sgr0)

echob() {
    echo "${bold}${@}${normal}"
}

citest() {
    echob "$@"
    $@ || exit 1
}

#!/usr/bin/env bash
echob() {
    echo "${bold}${1}${normal}"
}

citest() {
    echob "testing $@"
    "$@" || echob "failed" && exit 1
}

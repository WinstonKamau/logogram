#!/usr/bin/env bash

set -o errexit
set -o pipefail
# set -o nounset
# set -o xtrace

install_os_packages () {
    sudo apt-get -y upgrade
    sudo apt-get -y update
    sudo apt-get install -y python3-pip
    sudo apt-get install -y nginx
    sudo apt-get install -y supervisor
}

main () {
    install_os_packages
}

main "$@"
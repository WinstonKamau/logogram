#!/bin/bash

set -o errexit
set -o pipefail
# set -o nounset
# set -o xtrace

get_var() {
  local name="$1"

  curl -s -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/attributes/${name}"
}

install_ubuntu_packages() {
    apt-get update
    apt-get -y install curl
}

get_required_variables () {
    export HOST_NAME="$(get_var "hostName")"
}

install_chef_server() {
# create staging directories
if [ ! -d /drop ]; then
  mkdir /drop
fi
if [ ! -d /downloads ]; then
  mkdir /downloads
fi

# download the Chef server package
if [ ! -f /downloads/chef-server-core_12.17.33_amd64.deb ]; then
  echo "Downloading the Chef server package..."
  wget -nv -P /downloads https://packages.chef.io/files/stable/chef-server/12.19.31/ubuntu/16.04/chef-server-core_12.19.31-1_amd64.deb
fi

# configure hostname
sudo hostname "${HOST_NAME}"

# install Chef server
if [ ! $(which chef-server-ctl) ]; then
  echo "Installing Chef server..."
  sudo dpkg -i /downloads/chef-server-core_12.19.31-1_amd64.deb
  sudo chef-server-ctl reconfigure

  echo "Waiting for services..."
  until (curl -D - http://localhost:8000/_status) | grep "200 OK"; do sleep 15s; done
  while (curl http://localhost:8000/_status) | grep "fail"; do sleep 15s; done

  echo "Creating initial user and organization..."
  sudo chef-server-ctl user-create chefadmin Chef Admin admin@4thcoffee.com insecurepassword --filename /drop/chefadmin.pem
  sudo chef-server-ctl org-create 4thcoffee "Fourth Coffee, Inc." --association_user chefadmin --filename 4thcoffee-validator.pem
fi

echo "Your Chef server is ready!"
}

main() {
    install_ubuntu_packages
    get_required_variables
    install_chef_server
}

main
#!/usr/bin/env bash

set -o errexit
set -o pipefail
# set -o nounset
set -o xtrace

get_var() {
  local name="$1"

  curl -s -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/attributes/${name}"
}

get_required_variables () {
    export IP_ADDRESS="$(get_var "ipAddress")"
    export DJANGO_SETTINGS_MODULE=logogram.staging
    export SECRET_KEY="$(sudo openssl rand -hex 64)"
    export HOST="backend"
}

remove_precambrian_pip() {
    sudo apt-get remove python3-pip -y
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    pip3 install pipenv
}

clone_repository() {
    cd ~
    git clone https://github.com/WinstonKamau/logogram
    cd logogram
}

copy_nginx.conf() {
    sudo cp ~/logogram/devops/nginx.conf /etc/nginx/conf.d/
}

copy_supervisord_conf () {
    sudo cp ~/logogram/devops/supervisord.conf /etc/supervisor/supervisord.conf
    sudo cp ~/logogram/devops/start.sh /usr/local/bin/start-app
    sudo chmod +x /usr/local/bin/start-app
}


configure_logogram_site() {
    pipenv lock -r >requirements.txt
    pip3 install -r requirements.txt
    python3 ~/logogram/src/logogram/manage.py makemigrations
    python3 ~/logogram/src/logogram/manage.py migrate
    python3 ~/logogram/src/logogram/manage.py collectstatic --no-input
    sudo nginx -s reload
    sudo systemctl restart supervisor
}


main() {
    get_required_variables
    remove_precambrian_pip
    clone_repository
    copy_nginx.conf
    copy_supervisord_conf
    configure_logogram_site
}

main
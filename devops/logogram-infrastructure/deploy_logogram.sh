#!/usr/bin/env bash

set -o errexit
set -o pipefail
# set -o nounset
# set -o xtrace

get_var() {
  local name="$1"

  curl -s -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/attributes/${name}"
}

add_ssh_key () {
    echo "$(get_var "chefNodePublicKey")" >> /home/ubuntu/.ssh/authorized_keys
    echo "AllowUsers ubuntu" >> /etc/ssh/sshd_config
    echo "AuthorizedKeysFile      %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config
}

get_required_variables () {
    export IP_ADDRESS="$(get_var "ipAddress")"
    export DJANGO_SETTINGS_MODULE=logogram.staging
    export SECRET_KEY="$(sudo openssl rand -hex 64)"
    export HOST="127.0.0.1"
    export DATABASE_NAME="$(get_var "databaseName")"
    export USER="$(get_var "user")"
    export PASSWORD="$(get_var "password")"
    export POSTGRES_IP="$(get_var "postgresIp")"
}

remove_precambrian_pip() {
    wait_for_apt_lock
    sudo apt-get remove python3-pip -y
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    pip3 install pipenv
}

wait_for_apt_lock() {
    while [ "" = "" ]; do
        if sudo flock --timeout 60 --exclusive --close /var/lib/dpkg/lock apt-get -y -o Dpkg::Options::="--force-confold" upgrade
        then
            break
        fi
        sleep 1
        echo "Waiting for apt lock file to be deleted"
    done
}

clone_repository() {
    cd ~
    git clone https://github.com/WinstonKamau/logogram
    cd logogram
}

copy_nginx_conf() {
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
    sudo systemctl restart supervisor
    sudo nginx -s reload
}


main() {
    get_required_variables
    add_ssh_key
    remove_precambrian_pip
    clone_repository
    copy_nginx_conf
    copy_supervisord_conf
    configure_logogram_site
}

main
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
    export DATABASE_NAME="$(get_var "databaseName")"
    export USER="$(get_var "user")"
    export PASSWORD="$(get_var "password")"
    export POSTGRES_IP="$(get_var "postgresIp")"
}
start_app () {
    cd /root/logogram/src/logogram || exit
    gunicorn -b 0.0.0.0:8000 --error-logfile /var/log/logogram-error.log logogram.wsgi
}
main () {
    get_required_variables
    start_app
}
main "$@"
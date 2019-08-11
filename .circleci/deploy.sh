#!/usr/bin/env bash

set -o errexit
set -o pipefail

download_terraform() {
    wget https://releases.hashicorp.com/terraform/0.11.4/terraform_0.11.4_linux_amd64.zip
    unzip terraform_0.11.4_linux_amd64.zip
    chmod +x terraform
    sudo mv terraform /usr/local/bin/
}

prepare_deployment_script() {
    cd devops/account-folder
    touch account.json
    echo "${SERVICE_ACCOUNT}" > account.json
    touch ../chef-setup/chef-cookbooks/chef_node_ssh_key.pub
    echo "${SSH_PUB_KEY}" | base64 --decode -i > ../logogram-infrastructure/chef_node_ssh_key.pub
}


initialise_terraform() {
    cd ../logogram-infrastructure
    terraform init -lock=false -backend-config=bucket="${GCP_BUCKET}"
}

destroy_previous_infrastructure(){
    terraform destroy -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=region="${GCP_REGION}" -var=zone="${GCP_ZONE}" -var=database-name="${DATABASE_NAME}" -var=user="${DATABASE_USER}" -var=password="${DATABASE_PASSWORD}" -var=postgres-ip="${POSTGRES_IP}"
}

build_current_infrastructure() {
    terraform apply -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=region="${GCP_REGION}" -var=zone="${GCP_ZONE}" -var=database-name="${DATABASE_NAME}" -var=user="${DATABASE_USER}" -var=password="${DATABASE_PASSWORD}" -var=postgres-ip="${POSTGRES_IP}"
}

main() {
    download_terraform
    prepare_deployment_script
    initialise_terraform
    destroy_previous_infrastructure
    build_current_infrastructure
}

main "$@"
#! /usr/bin/bash

ssh_key_creation () {
    if [ -f "chef_node_ssh_key" ] && [ -f "chef_node_ssh_key.pub" ]; then
        echo "There already exists a private key and a public key for your nodes"
        if_key_exists
    elif [ -f "chef_node_ssh_key" ] && [ ! -f "chef_node_ssh_key.pub" ]; then
        echo "There exists a private key but no public key"
        if_key_exists
    elif [ ! -f "chef_node_ssh_key" ] && [ -f "chef_node_ssh_key.pub" ]; then
        echo "There exists a public key but no private key"
        if_key_exists
    else
        create_ssh_key
    fi
}

if_key_exists () {
    echo -n "Would you like to create new private and public keys? Enter y for Yes and n for No: "
    answer=
    while [[ ! $answer ]];do
    read -r -n 1 answer_argument
        if [[ $answer_argument = [Yy] ]];then
            answer="yes"
            rm -f chef_node_ssh_key
            rm -f chef_node_ssh_key.pub
            create_ssh_key
        elif [[ $answer_argument = [Nn] ]];then
            answer="no"
            printf "\nAborting\n"
        else
            printf "\nEnter \"y'\" for \"Yes\" and \"n\" for \"No\". Answer?"
        fi
    done
}

create_ssh_key() {
    ssh-keygen -f chef_node_ssh_key -C "" -P ""
    mv chef_node_ssh_key ../chef-setup/chef-cookbooks/
}

ssh_key_creation

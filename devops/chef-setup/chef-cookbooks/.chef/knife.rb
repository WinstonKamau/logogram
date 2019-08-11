current_dir = File.dirname(__FILE__)
hostname = ENV['HOSTNAME']
fail KeyError, 'The HOSTNAME environment variable is not set.' unless hostname
log_level                 :debug
log_location              STDOUT
node_name                 "chefadmin"
client_key                "#{current_dir}/chefadmin.pem"
chef_server_url           "https://#{hostname}/organizations/4thcoffee"
cookbook_path             ["#{current_dir}/../"]
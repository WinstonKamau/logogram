#
# Cookbook:: logogram-os
# Recipe:: default
#
# Copyright:: 2019, The Authors, All Rights Reserved.

apt_update 'Update the apt cache on chef client runs' do
  action :update
end

package 'nginx' do
  version '1.10.*'
end

package 'supervisor' do
  version '3.2.*'
end

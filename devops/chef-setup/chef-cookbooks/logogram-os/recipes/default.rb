#
# Cookbook:: logogram-os
# Recipe:: default
#
# Copyright:: 2019, The Authors, All Rights Reserved.

apt_update 'Update the apt cache on chef client runs' do
    action :update
  end
package 'python3-pip' do
    version '' 
end
package 'nginx' do
    version ''
end
package 'supervisor' do
    version ''
end

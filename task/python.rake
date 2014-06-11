# NOTE: pre_build/pre_install directories are created by pip.

directory 'core/site-packages/pre_install' do |task|
  sh "pip install --requirement=pre_install_requirements.txt " \
    "--target=#{task.name} --ignore-installed"
end

namespace :python do
  desc 'Installs Python packages in a local directory'
  task :compile => ['core/site-packages/pre_install']
end

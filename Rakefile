require 'bundler/gem_tasks'
require 'rake/clean'

CLEAN.include(
  'tmp/*',
  'pkg',
  '**/*.pyo',
  '**/*.pyc',
  'core/site-packages/pre_build',
  'core/site-packages/pre_install'
)

Dir.glob(File.expand_path('../task/*.rake', __FILE__)) do |task|
  import(task)
end

task :default => :test

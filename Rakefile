require 'bundler/gem_tasks'
require 'opener/build-tools/tasks/python'
require 'opener/build-tools/tasks/clean'

require_relative 'ext/hack/support'

desc 'Lists all the files of the Gemspec'
task :files do
  gemspec = Gem::Specification.load('opener-coreference-base.gemspec')

  puts gemspec.files.sort
end

desc 'Verifies the requirements'
task :requirements do
  verify_requirements
end

desc 'Cleans up the repository'
task :clean => [
  'python:clean:bytecode',
  'python:clean:packages',
  'clean:tmp',
  'clean:gems'
]

desc 'Compile all C code'
task :compile_c do
  compile_vendored_code
end

desc 'Compiles everything'
task :compile => [:compile_c, 'python:compile']

desc 'Runs the tests'
task :test => :compile do
  sh('cucumber features')
end

desc 'Performs preparations for building the Gem'
task :before_build => [:requirements, 'python:clean:bytecode'] do
  path = File.join(PYTHON_SITE_PACKAGES, 'pre_build')

  install_python_packages(PRE_BUILD_REQUIREMENTS, path)
end

task :build   => :before_build
task :default => :test

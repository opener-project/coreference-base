require_relative '../../lib/opener/coreferences/en'
require 'rspec/expectations'
require 'tempfile'

def kernel_root
  File.expand_path("../../../", __FILE__)
end

def kernel
  return Opener::Coreferences::EN.new
end

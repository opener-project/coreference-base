require_relative '../../lib/opener/coreferences/base'
require 'rspec/expectations'
require 'tempfile'

def kernel_root
  File.expand_path("../../../", __FILE__)
end

def kernel(args = [])
  return Opener::Coreferences::Base.new(:args => args)
end

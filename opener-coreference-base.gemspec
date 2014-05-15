require File.expand_path('../lib/opener/coreferences/base/version', __FILE__)

Gem::Specification.new do |gem|
  gem.name        = 'opener-coreference-base'
  gem.version     = Opener::Coreferences::Base::VERSION
  gem.authors     = ['development@olery.com']
  gem.summary     = 'Coreference resolution for various languages.'
  gem.description = gem.summary
  gem.has_rdoc    = 'yard'
  gem.extensions  = ['ext/hack/Rakefile']

  gem.required_ruby_version = '>= 1.9.2'

  gem.files = Dir.glob([
    'core/site-packages/pre_build/**/*',
    'ext/**/*',
    'lib/**/*',
    '*.gemspec',
    '*_requirements.txt',
    'README.md'
  ]).select { |file| File.file?(file) }

  gem.executables = Dir.glob('bin/*').map { |file| File.basename(file) }

  gem.add_dependency 'rake'
  gem.add_dependency 'opener-build-tools', ['>= 0.2.7']
  gem.add_dependency 'nokogiri'

  gem.add_development_dependency 'cucumber'
  gem.add_development_dependency 'rspec'
end

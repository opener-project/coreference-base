require File.expand_path('../lib/opener/coreferences/en/version', __FILE__)

Gem::Specification.new do |gem|
  gem.name        = 'opener-coreference-en'
  gem.version     = Opener::Coreferences::EN::VERSION
  gem.authors     = ['development@olery.com']
  gem.summary     = 'Coreference resolution for the English language.'
  gem.description = gem.summary
  gem.has_rdoc    = 'yard'

  gem.required_ruby_version = '>= 1.9.2'

  gem.files       = `git ls-files`.split("\n").sort
  gem.executables = gem.files.grep(%r{^bin/}).map{ |f| File.basename(f) }
  gem.test_files  = gem.files.grep(%r{^(test|spec|features)/})

  gem.add_dependency 'rake'
  gem.add_dependency 'opener-build-tools', ['>= 0.2.7']

  gem.add_development_dependency 'cucumber'
  gem.add_development_dependency 'rspec'
end

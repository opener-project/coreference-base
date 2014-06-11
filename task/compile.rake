desc 'Verifies requirements and compiles the core'
task :compile => ['requirements', 'python:compile']

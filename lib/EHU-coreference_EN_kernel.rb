require 'tempfile'

module Opener
  module Kernel
    module EHU
      module Coreference 
          class EN 
            VERSION = "0.0.2"

            attr_reader :kernel, :lib

            def initialize
              core_dir    = File.expand_path("../core", File.dirname(__FILE__))

              @kernel      = core_dir+'/process.py'
            end

            def command(opts={})
              arguments = opts[:arguments] || []
              #arguments << "-n" if opts[:test]

              "cat #{opts[:input]} | python #{kernel} #{opts[:input]} #{arguments.join(' ')}"

            end

          end
      end
    end
  end
end



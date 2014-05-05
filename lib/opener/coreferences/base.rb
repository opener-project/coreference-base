require 'open3'
require 'nokogiri'

require_relative 'base/version'

module Opener
  module Coreferences
    ##
    # Coreference class for various languages such as English and Spanish.
    #
    # @!attribute [r] args
    #  @return [Array]
    # @!attribute [r] options
    #  @return [Hash]
    #
    class Base
      attr_reader :args, :options

      ##
      # Returns the default language to use.
      #
      # @return [String]
      #
      DEFAULT_LANGUAGE = 'en'.freeze

      ##
      # @param [Hash] options
      #
      # @option options [Array] :args The commandline arguments to pass to the
      #  underlying Java code.
      #
      def initialize(options = {})
        
        @args    = options.delete(:args) || []
        @options = options
      end

      ##
      # Returns a String containing the command used to execute the kernel.
      #
      # @return [String]
      #
      def command
        return "#{adjust_python_path} python -E -OO -m #{kernel} #{args.join(' ')}"
      end

      ##
      # Runs the command and returns the output of STDOUT, STDERR and the
      # process information.
      #
      # @param [String] input The input to process.
      # @return [Array]
      #
      def run(input)
        @args << ["--language #{language(input)}"]
        Dir.chdir(core_dir) do
          capture(input)
        end
      end

      ##
      # Runs the command and takes care of error handling/aborting based on the
      # output.
      #
      # @see #run
      #
      def run!(input)
        stdout, stderr, process = run(input)

        if process.success?
          puts stdout

          STDERR.puts(stderr) unless stderr.empty?
        else
          abort stderr
        end
      end

      protected
      ##
      # @return [String]
      #
      def adjust_python_path
        site_packages =  File.join(core_dir, 'site-packages')
        "env PYTHONPATH=#{site_packages}:$PYTHONPATH"
      end
      
      def capture(input)
        Open3.popen3(*command.split(" ")) {|i, o, e, t|
          out_reader = Thread.new { o.read }
          err_reader = Thread.new { e.read }
          i.write input
          i.close
          [out_reader.value, err_reader.value, t.value]
        }
      end

      ##
      # @return [String]
      #
      def core_dir
        return File.expand_path('../../../../core', __FILE__)
      end

      ##
      # @return [String]
      #
      def kernel
        return 'corefgraph.process.file'
      end
      
      ##
      # @return the language from the KAF
      #
      def language(input)
        document = Nokogiri::XML(input)
        language = document.at('KAF').attr('xml:lang')
        return language
      end
    end # Base
  end # Coreferences
end # Opener

require 'open3'

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
        return "python -E -O #{kernel} -l #{language} #{args.join(' ')}"
      end

      ##
      # Runs the command and returns the output of STDOUT, STDERR and the
      # process information.
      #
      # @param [String] input The input to process.
      # @return [Array]
      #
      def run(input = nil)
        unless File.file?(kernel)
          raise "The Python kernel (#{kernel}) does not exist"
        end

        return Open3.capture3(command, :stdin_data => input, :chdir => core_dir)
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
      def language
        return options[:language] || DEFAULT_LANGUAGE
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
        return File.join(core_dir, 'process.py')
      end
    end # Base
  end # Coreferences
end # Opener

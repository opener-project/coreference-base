#encoding utf-8
"""
Implements Stanford Multi-Sieve Pass Coreference System as their 2013 Computational Linguistics paper

"""
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>, Rodrigo Agerri <rodrigo.agerri@ehu.es>'


import argparse
import logging


def main():
    import properties
    arguments = parse_cmd_arguments()
    properties.set_lang(arguments.language)
    import sys
    import codecs
    from text_processor import TextProcessor

    if arguments.input:
        input_text = codecs.open(filename=arguments.input[0], mode="r").read()
        parse_tree = codecs.open(filename=arguments.input[1], mode="r").read()
    else:
        input_text = sys.stdin.read()
        parse_tree = codecs.open(filename=arguments.parse_tree, mode="r").read()

    processor = TextProcessor()
    processor.process_text((input_text.strip(), parse_tree.strip()))

    processor.store_analysis(arguments.encoding, arguments.language, arguments.version,
                   arguments.linguistic_parser_name, arguments.linguistic_parser_version,
                   arguments.linguistic_parser_layer)


def parse_cmd_arguments(logger=logging.getLogger('argsparse')):
    """ Parse command line arguments and put options into a object."""
    logger.debug("Creating parser")
    parser = argparse.ArgumentParser(description="Process a text file or a \
        directory tree of text file through freeling processors and \
        analyzers", fromfile_prefix_chars="@")
    # Sources
    parser.add_argument('-files', '-i', nargs=2, dest='input', action='store', default=None)
    parser.add_argument('-treebank', '-s', dest='parse_tree', action='store', default=None)
    parser.add_argument('-language', '-l', dest='language', action='store', default="en")
    parser.add_argument('-version', '-v', dest='version', action='store', default="v1.opener")
    parser.add_argument('-encoding', '-e', dest='encoding', action='store', default="UTF-8")
    parser.add_argument('-linguisticParserName', '-lpn', dest='linguistic_parser_name',
                        action='store', default="corefgraphEN")
    parser.add_argument('-linguisticParserVersion', '-lpv', dest='linguistic_parser_version',
                        action='store', default="0.8")
    parser.add_argument('-linguisticParserLayer', '-lpl', dest='linguistic_parser_layer',
                        action='store', default="coreference")
    parser.add_argument('-singleton', action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    main()

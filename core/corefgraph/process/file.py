#!/usr/bin/python
# coding=utf-8
"""
Implements Stanford Multi-Sieve Pass Coreference System as their 2013 Computational Linguistics paper

"""

__author__ = 'Josu Bermúdez <josu.bermudez@deusto.es>, Rodrigo Agerri <rodrigo.agerri@ehu.es>'

import sys
import getopt
import os

this_folder = os.path.dirname(os.path.realpath(__file__))

# This updates the load path to ensure that the local site-packages directory
# can be used to load packages (e.g. a locally installed copy of lxml).
sys.path.append(os.path.join(this_folder, '../../site-packages/pre_build'))
sys.path.append(os.path.join(this_folder, '../../site-packages/pre_install'))

from corefgraph import properties

from lxml import etree
import argparse
import logging
import logging.config
import codecs

logger = logging.getLogger("FILE_PROCESSOR")


def process(config, text, parse_tree, speakers_list, output):
    """Process a document through the corefgraph system.info

    :param config: The parameters used to tune the resolution and output format.
    :param text: The KAF file of the document
    :param parse_tree: A list o treebank parse trees
    :param speakers_list: A list of the speaker per token.
    :param output: The stream where the output is write.
    """
    # This is because properties is used to spread the language all over the module
    logger.info("Setting language to %s", config.language)
    properties.set_lang(config.language)
    from corefgraph.text_processor import TextProcessor
    # End of voodoo
    processor = TextProcessor(verbose=config.verbose, reader=config.reader, secure_tree=config.secure_tree,
                              lang=config.language, sieves=config.sieves, sieves_options=config.sieves_options,
                              extractor_options=config.extractor_options, singleton=config.singleton)

    document = (text, parse_tree, speakers_list)
    processor.process_text(document)
    if not config.linguistic_parser_name:
        config.linguistic_parser_name = "corefgraph-"+config.language
    if config.conll:
        processor.store_analysis_conll(stream=output, document_id=config.document_id, part_id=config.part_id)
    else:
        if config.reader == "NAF":
            processor.store_analysis_naf(
                stream=output, encoding=config.encoding, language=config.language, version=config.version,
                lp_name=config.linguistic_parser_name, lp_version=config.linguistic_parser_version,
                lp_layer=config.linguistic_parser_layer, time_stamp=config.time_stamp)
        elif config.reader == "KAF":
            processor.store_analysis_kaf(
                stream=output, encoding=config.encoding, language=config.language, version=config.version,
                lp_name=config.linguistic_parser_name, lp_version=config.linguistic_parser_version,
                lp_layer=config.linguistic_parser_layer, time_stamp=config.time_stamp)


def main():
    """ Invoked when the module is uses directly from as CLI tool.
    Uses the argparse from def generate_parser() .

    @return: NOTHING
    """
    arguments = generate_parser().parse_args()

    if arguments.input:
        input_text = codecs.open(filename=arguments.input, mode="r").read()
    else:
        logger.info("kaf from standard input")
        input_text = sys.stdin.read()
    if arguments.parse_tree:
        parse_tree = codecs.open(filename=arguments.parse_tree, mode="r").read()
    else:
        parse_tree = None

    if arguments.speakers:
        logger.info("No speaker annotation")
        speakers_list = codecs.open(filename=arguments.speakers, mode="r").read()
    else:
        speakers_list = None
    process(config=arguments, text=input_text, parse_tree=parse_tree, speakers_list=speakers_list, output=sys.stdout)


def generate_parser():
    """ Parse command line arguments and get values needed to process a file."""
    logger.debug("Creating parser")
    parser = argparse.ArgumentParser(description="Process a text file or a \
        directory tree of text file through freeling processors and \
        analyzers", fromfile_prefix_chars="@")
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.add_argument('--document_id', dest='document_id', action='store', default=None)
    parser.add_argument('--part_id', dest='part_id', action='store', default=None)
    parser.add_argument('--file', "-f", dest='input', action='store', default=None)
    parser.add_argument('--treebank', dest='parse_tree', action='store', default=None)
    parser.add_argument('--speakers', dest='speakers', action='store', default=None)
    parser.add_argument('--language', dest='language', action='store', default="en")
    parser.add_argument('--unsafe_tree', dest='secure_tree', action='store_false')
    parser.add_argument('--reader', dest='reader', action='store', default="KAF")
    parser.add_argument('--conll', dest='conll', action='store_true')
    parser.add_argument('--no_filter_same_head', dest='no_filter_same_head', action='store_true')
    parser.add_argument('--sieves', dest='sieves', nargs='*', action="store", default=[],
                        help="The plain name of the sieves that must be used.")
    parser.add_argument('--sieves_options', dest='sieves_options', action="append", default=[],
                        help="The options passed to the sieves.")
    parser.add_argument('--extractor_options', dest='extractor_options', nargs='*', action="store", default=[],
                        help="The options used during mention extraction.")
    parser.add_argument('--version', dest='version', action='store', default="v1.opener")
    parser.add_argument('--encoding', dest='encoding', action='store', default="UTF-8")
    parser.add_argument('--linguisticParserName', dest='linguistic_parser_name',
                        action='store', default=None)
    parser.add_argument('--linguisticParserVersion', dest='linguistic_parser_version',
                        action='store', default="0.8")
    parser.add_argument('--linguisticParserLayer', dest='linguistic_parser_layer',
                        action='store', default="coreference")
    parser.add_argument('--time_stamp', dest='time_stamp',
                        action='store', default=None)
    parser.add_argument('--singleton', action='store_true')
    return parser


if __name__ == "__main__":
    main()

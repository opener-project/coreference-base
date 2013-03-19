#encoding utf-8
"""
Process a corpus of ontonotes or directory form and generates a output in CONLL format.

If ontonotes is used evalutates the correfrerence,
"""
from graph.kaf import KafAndTreeGraphBuilder
from output.kafwritter import KafDocument

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>,Rodrigo Agerri <rodrigo.agerri@ehu.es>'

import argparse
import logging
import sys
import simplejson

from output.progressbar import ProgressBar, Fraction

from multisieve.core import CoreferenceProcessor
from features.grendel import GenderNumberExtractor


class TextProcessor:
    """ Process a single text or corpus with several NLP stages managing the result as graphs.
    """

    def __init__(self, logger=logging.getLogger("main")):
        self.logger = logger
        # Graph builder and manager
        self.graph_builder = KafAndTreeGraphBuilder()
        # Coreference process
        self.gender_extractor = GenderNumberExtractor()

    def reset_graph(self):
        """Recreates the graph and the elements that used a graph reference.

        """
        # Graph attributes
        self.graph = self.graph_builder.new_graph()
        self.CP = CoreferenceProcessor(self.graph, self.graph_builder, singletons=True,
                                       logger=self.logger)
        self.graph_builder.set_graph(self.graph)
        self.gender = self.graph_builder.get_property("gender")
        self.number = self.graph_builder.get_property("number")
        self.animacy = self.graph_builder.get_property("animate")

        self.pos = self.graph_builder.get_property("pos")
        self.form = self.graph_builder.get_property("form")
        self.label = self.graph_builder.get_property("label")
        self.ner = self.graph_builder.get_property("ner")

    def build_graph(self, document):
        """ Build a graph form external parser.
        """
        sentences_parsed = self.graph_builder.preprocess_sentences(graph=self.graph, document=document)
        # Add each sentence to de graph
        widgets = ['Building Graph: ', Fraction()]
        progress_bar = ProgressBar(widgets=widgets, maxval=len(sentences_parsed), force_update=True).start()
        for index, sentence in enumerate(sentences_parsed):
            # Dependency graph construction
            sentence_root = self.graph_builder.process_sentence(
                graph=self.graph, sentence=sentence,sentence_namespace="text@{0}".format(index), root_index=index)
            # Generate Coreference Candidatures for the sentence
            self.CP.process_sentence(sentence_root)

        progress_bar.finish()
        # With the graph populated

    def post_process_document(self):
        """ Prepare the graph for output.
        """
        error_message = False
        candidatures = self.CP.get_candidates()
        widgets = ['Setting gender ', Fraction()]
        progress_bar = ProgressBar(widgets=widgets, maxval=len(candidatures), force_update=True).start()
        for index, (entity, candidates) in enumerate(candidatures):
            mention = entity[0]
            pos = self.pos[mention]
            ner = self.ner[mention]
            try:
                form = self.form[self.graph_builder.get_chunk_head_word(mention)]
            except Exception as ex:
                if not error_message:
                    sys.stderr.write("WARNING NO HEAD FOUND without heads strict head match and pronoun sieve will not"
                                 " work correctly\n")
                error_message = True
                form = self.form[mention]
            self.gender[mention] = self.gender_extractor.get_gender(form=form, pos=pos)
            self.number[mention] = self.gender_extractor.get_number(form=form, pos=pos, ner=ner)
            self.animacy[mention] = self.gender_extractor.get_animacy(form=form, pos=pos, ner=ner)
            progress_bar.update(index + 1)
        progress_bar.finish()
        self.CP.resolve()

        self.graph_builder.documentup()

    def show_graph(self):
        """Show the graph in graphviz screen"""
        self.graph_builder.show_graph()

    def process_text(self, original_text):
        self.reset_graph()
        self.build_graph(original_text)
        self.post_process_document()


def clean_treebank(treebank_file):
    """Remove from treebank file all spurious character."""
    treebank_file = treebank_file.strip()
    return treebank_file


def main():
    import sys

    arguments = parse_cmd_arguments()

    if arguments.input:
        input_text = open(arguments.input[0], "r").read()
        parse_tree = open(arguments.input[1], "r").read()
    else:
        input_text = sys.stdin.read()
        parse_tree = open(arguments.parse_tree, "r").read()


    parse_tree = clean_treebank(parse_tree)

    processor = TextProcessor()
    processor.process_text((input_text, parse_tree))

    store_analysis(processor.graph, arguments.encoding, arguments.language, arguments.version,
                   arguments.linguistic_parser_name, arguments.linguistic_parser_version,
                   arguments.linguistic_parser_layer)
    processor.show_graph()
    input("Pulse una tecla")


def store_analysis(result, encoding, language, version, lp_name, lp_version, lp_layer,):
    """ Stores a corpus analysis results into files.

     options -- The format and other storing options. Expected as a plain object with options as attributes.
     results -- the results of analyzing a corpus. Expected as a list of tuples(file_name, list_of_freeling_elements).
    """
    writer = KafDocument(stream=sys.stdout)
    writer.store(result, encoding=encoding, language=language, version=version, linguistic_parsers=[
        (lp_name, lp_version, lp_layer)])


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

    return parser.parse_args()

if __name__ == "__main__":
    main()


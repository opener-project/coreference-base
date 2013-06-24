#encoding utf-8
"""
Process a corpus of ontonotes or directory form and generates a output in CONLL format.

If ontonotes is used evalutates the correfrerence,
"""
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>, Rodrigo Agerri rodrigo.agerri@ehu.es'

import subprocess
import argparse
import logging
import os

from output.progressbar import ProgressBar, Fraction

from multisieve.core import CoreferenceProcessor
from output.conllwriter import ConllDocument
from graph.stanfordParser import StanfordCoreNLPGraphBuilder
from graph.conll import OntonotesGraphBuilder
from features.ilf import ContextGenerator
from graph.utils import GraphWrapper
from features.grendel import GenderNumberExtractor
from input.ontonotes import OntoNotesReader
import sys


class TextProcessor:
    """ Process a single text or corpus with several NLP stages managing the result as graphs.
    """
    separator = "_"

    verbose = False

    def __init__(self, options, logger=logging.getLogger("main")):
        self.logger = logger
        self.options = options
        # Graph builder and manager
        if options.ontonotes_config:
            self.on_reader = OntoNotesReader(config_file=options.ontonotes_config)
            self.graph_builder = OntonotesGraphBuilder(self.on_reader.corpus)
        else:
            self.graph_builder = StanfordCoreNLPGraphBuilder(ip=options.host, port=int(options.port),
                                                             logger=self.logger)
            # Empty Graph
        # Context Graph constructor
        self.CG = ContextGenerator(self.graph_builder)
        # Coreference process
        self.gender_extractor = GenderNumberExtractor()

    def reset_graph(self):
        """Recreates the graph and the elements that used a graph reference.

        """
        # Graph attributes
        self.graph = self.graph_builder.new_graph()
        self.CP = CoreferenceProcessor(self.graph, self.graph_builder, self.options.singletons,
                                       logger=self.logger, verbose=self.verbose)
        self.gender = GraphWrapper.node_property("gender", self.graph)
        self.number = GraphWrapper.node_property("number", self.graph)
        self.animacy = GraphWrapper.node_property("animate", self.graph)

        self.pos = GraphWrapper.node_property("pos", self.graph)
        self.form = GraphWrapper.node_property("form", self.graph)
        self.label = GraphWrapper.node_property("lemma", self.graph)
        self.ner = GraphWrapper.node_property("ner", self.graph)

    def build_graph_ontonotes(self, document, document_namespace):
        """ Build graph with using the info in a ontonotes corpus.
        """
        # Add each sentence to de graph
        widgets = ['Building Graph: ', Fraction()]
        pbar = ProgressBar(widgets=widgets, maxval=len(document), force_update=True).start()
        for index, sentence in enumerate(document.tree_document[:7]):
            # Dependency graph construction
            sentence_root = self.graph_builder.process_sentence(
                graph=self.graph,
                sentence=sentence,
                root_index=index
            )
            # Context Graph construction
            # Generate accessibility
            #sentence = CG.process_graph(graph, sentence_root, graph)
            # Generate Coreference Candidatures for the sentence
            self.CP.process_sentence(sentence_root)
            pbar.update(index + 1)
        pbar.finish()
        # With the graph populated
        # Set the gender

    def build_graph(self, document, document_namespace):
        """ Build a graph form external parser.
        """
        sentences_parsed = self.graph_builder.parse_source(document)
        # Add each sentence to de graph
        widgets = ['Building Graph: ', Fraction()]
        pbar = ProgressBar(widgets=widgets, maxval=len(sentences_parsed), force_update=True).start()
        for index, sentence in enumerate(sentences_parsed):
            # Dependency graph construction
            sentence_root = self.graph_builder.process_sentence(graph=self.graph, sentence=sentence, root_index=index,
                                                                sentence_namespace="{0}{2}{1}".format(
                                                                    document_namespace, index, self.separator))
            # Context Graph construction
            # Generate accessibility
            #sentence = CG.process_graph(graph, sentence_root, graph)
            # Generate Coreference Candidatures for the sentence
            self.CP.process_sentence(sentence_root)
            pbar.update(index + 1)
        pbar.finish()
        # With the graph populated
        # Set the gender

    def post_process_document(self):
        """ Prepare the graph for output.
       """
        error_message = False
        candidatures = self.CP.get_candidates()
        widgets = ['Setting gender ', Fraction()]
        progress_bar = ProgressBar(widgets=widgets, maxval=len(candidatures), force_update=True).start()
        for index, (entity, candidates, log) in enumerate(candidatures):

            mention = entity[0]
            pos = self.pos[mention]
            ner = self.ner[mention]
            #
            try:
                head_word_form = self.form[self.graph_builder.get_chunk_head_word(mention)]
            except Exception as ex:
                if not error_message:
                    sys.stderr.write("WARNING NO HEAD FOUND without heads strict head match and pronoun sieve will not"
                                     " work correctly\n")
                error_message = True
                head_word_form = self.form[mention]
            self.gender[mention] = self.gender_extractor.get_gender(form=head_word_form, pos=pos)
            self.number[mention] = self.gender_extractor.get_number(form=head_word_form, pos=pos, ner=ner)
            self.animacy[mention] = self.gender_extractor.get_animacy(form=head_word_form, pos=pos, ner=ner)

            progress_bar.update(index + 1)
            sys.stderr.write("{0} | {1} | {2} | {3} | {4}\n".format(self.form[mention], head_word_form,
                                                                    self.gender[mention], self.number[mention],
                                                                    self.animacy[mention]))
        progress_bar.finish()
        self.CP.resolve_text()

        self.graph_builder.statistics_document_up()

    def process_corpus(self):
        """ Analyze text files pointed by dirs an files attributes or the pointed ontonotes corpus.

        Analysis and options determines by argument passed.
        for further info call the script width --help or -h parameters.
        """
        # Ontonotes config file appears process the ontonotes corpus

        results = {}
        if self.options.ontonotes_config:
            for sub_corpus in self.on_reader.corpus:
                self.logger.info("loading corpus: %s ....", sub_corpus)
                for document in self.on_reader.get_corpus_documents(sub_corpus):
                    self.reset_graph()
                    self.logger.info("loading document: %s ....", document)
                    #self.build_graph_ontonotes(document, sub_corpus)
                    self.build_graph_ontonotes(document, document.document_id.split("@")[0])
                    self.post_process_document()
                    #self.process(text=document.text.split("\n"),  text_namespace=document.document_id)
                    output_name = self.options.ontonotes_dest + document.document_id.split("@")[0]
                    self.store_analysis(file_name=output_name, result=self.graph)
                    results[document.document_id.split("@")[0]] = self.graph
            return results

        else:
            # Generate unique file list
            no_filter_extensions = self.options.extensions in ("*", "*.*")
            # Add the selected files
            file_list = self.options.files or []
            # Add the files included in the directories
            for directory in self.options.directories:
                for root, dirs, files in os.walk(directory):
                    # In case of no recursive adding
                    if not self.options.recursive:
                        del dirs[:]
                    for fullname in files:
                        name, ext = os.path.splitext(fullname)
                        # Filter , if necessary, the included files
                        if ext in self.options.extensions or no_filter_extensions:
                            file_list.append(os.path.join(root, fullname))

            # Process all files in the list
            for file_name in file_list:
                self.reset_graph()
                self.logger.info("loading file: %s ....", file_name)
                original_text = open(file_name).read()
                self.build_graph(original_text.split("\n"), "file@" + file_name)
                self.post_process_document()
                self.store_analysis(file_name, self.graph)
            return results

    def show_graph(self):
        """Show the graph in graphviz screen"""
        GraphWrapper.showGraph(self.graph, vcolor='color', vshape="shape")

    def evaluate_corpus(self, results):
        """ Evaluate the result of the system in coreference using the CONLL evaluation script.
        """
        for filename, result in results.items():
            key_filename = os.path.join(self.options.key_path, filename) + self.options.key_file_extension
            result_filename = os.path.join(self.options.ontonotes_dest, filename) + self.options.output_extension
            self.evaluate_file(key_file=key_filename, result_file=result_filename)

    def evaluate_file(self, key_file, result_file):
        """ Evaluate a file  in coreference using the CONLL evaluation script.
        """
        output_file = open('results.out', 'a')
        cwd, scorer = os.path.split(self.options.scorer_path)
        self.logger.debug("Scorer:%s", scorer)
        self.logger.debug("In : %s", cwd)
        self.logger.info("Evaluating  %s against %s", result_file, key_file)
        self.logger.info("Stored in:%s", output_file)
        self.logger.debug("CMD: %s all %s %s none", self.options.scorer_path, key_file, result_file)
        subprocess.call(["./" + scorer, "all", key_file, result_file, "none"], stdout=output_file, cwd=cwd)

    def store_analysis(self, file_name, result):
        """ Stores a corpus analysis results into files.

         options -- The format and other storing options. Expected as a plain object with options as attributes.
         results -- the results of analyzing a corpus. Expected as a list of tuples(file_name, list_of_freeling_elements).
        """
        self.logger.info("Saving %s", file_name)
        tail, base_name = os.path.split(file_name)
        # Secure no blank tail
        tail = tail or "./"
        name, ext = os.path.splitext(base_name)
        # If path not exist create it
        if not os.access(tail, os.F_OK): os.makedirs(tail)
        with ConllDocument(filename=os.path.join(tail, name + self.options.output_extension), document_id=name) as conll_document:
            conll_document.store(result)

    def print_stats(self):
        word, sentences, documents = self.graph_builder.get_stats()
        print "Words:{0}\nSentences:{1}\nDocuments:{2}\n".format(word, sentences, documents)


def main():
    """ Read Form command line the options and files and process it through a processor.
    """
    # Logging
    logger = logging.getLogger("Main")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    # Get CLI arguments
    arguments = parse_cmd_arguments(logger)
    # Process corpus
    processor = TextProcessor(arguments, logger=logger)
    results = processor.process_corpus()
    # Evaluate corpus
    if arguments.evaluation:
        processor.evaluate_corpus(results)
        # Show graph
    if arguments.graph:
        processor.show_graph()
        raw_input("Press ANY KEY to Exit")
        # Alert at end
    processor.print_stats()
    print "\a"


def parse_cmd_arguments(logger=logging.getLogger('argsparse')):
    """ Parse command line arguments and put options into a object."""
    logger.debug("Creating parser")
    parser = argparse.ArgumentParser(description="Process a text file or a \
        directory tree of text file through freeling processors and \
        analyzers", fromfile_prefix_chars="@")
    # Sources
    parser.add_argument('-ontonotes', dest='ontonotes_config', action="store", default=None)
    parser.add_argument('-files', '-f', dest="files",  nargs='*', action='store', default=[])
    parser.add_argument('-dir', dest='directories', nargs='*', action="store", default=[])
    parser.add_argument('-no_recursive', dest='recursive', action='store_false')

    # Processing
    parser.add_argument('-lang', dest='language', action='store', default='en')
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('-graph', dest='graph', action='store_true')

    # Stanford
    parser.add_argument('-host', dest='host', action='store', default='127.0.0.1')
    parser.add_argument('-port', dest='port', action='store', default=8080)

    # Ontonotes
    parser.add_argument('-ontonotes_dest', dest='ontonotes_dest', action="store", default="/tmp/ontonotes/")

    # Evaluation
    parser.add_argument('-scorer', dest='scorer_path', action="store", default="resources/scripts/scorer.pl")
    parser.add_argument('-key', dest='key_file_extension', action='store', default='.conll.plain')
    parser.add_argument('-key_path', dest='key_path', action='store', default='./keys/data/english/annotations')

    parser.add_argument('-off_evaluation', dest='evaluation', action='store_false')
    parser.add_argument('-singletons', dest='singletons', action='store_true')

    # Store Results
    parser.add_argument('-ext', nargs='*', dest='extensions', action='store', default=('.txt',))
    parser.add_argument('-out', dest='output_extension', action='store', default='.out')
    parser.add_argument('-encoding', dest='encoding', action='store', default='utf8')

    return parser.parse_args()


if __name__ == "__main__":
    main()

import logging
import sys
from features.grendel import GenderNumberExtractor
from graph.kafx import KafAndTreeGraphBuilder, SyntacticTreeUtils
from multisieve.core import CoreferenceProcessor
from output.kafwritter import KafDocument
from output.progressbar import Fraction, ProgressBar

__author__ = 'nasgar'


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
        graph = self.graph_builder.new_graph()
        self.graph = graph
        self.CP = CoreferenceProcessor(graph, singletons=False, logger=self.logger)
        self.graph_builder.set_graph(graph)
        self.tree_utils = SyntacticTreeUtils(graph)

    def build_graph(self, document):
        """ Build a graph form external parser.
        """
        sentences_parsed = self.graph_builder.preprocess_sentences(graph=self.graph, document=document)
        # Add each sentence to de graph
        widgets = ['Building Graph: ', Fraction()]
        #progress_bar = ProgressBar(widgets=widgets, maxval=len(sentences_parsed), force_update=True).start()
        #for index, sentence in enumerate(sentences_parsed):
        for index, sentence in enumerate(sentences_parsed):
            sentence = self.clean_treebank(sentence)
            # Dependency graph construction
            sentence_root = self.graph_builder.process_sentence(
                graph=self.graph, sentence=sentence, sentence_namespace="text@{0}".format(index), root_index=index)
            # Generate Coreference Candidatures for the sentence
            self.CP.process_sentence(sentence_root)

            #progress_bar.finish()
            # With the graph populated

    def post_process_document(self):
        """ Prepare the graph for output.
        """
        error_message = False
        candidatures = self.CP.get_candidates()
        if len(candidatures):
            widgets = ['Setting gender ', Fraction()]
            progress_bar = ProgressBar(widgets=widgets, maxval=len(candidatures) or 1, force_update=True).start()
            with open("mentions.out", "w") as out:
                for index, entity in enumerate(candidatures):
                    # The entities are singletons yet
                    mention = self.graph.node[entity[0]]
                    if "pos" in mention:
                        pos = mention["pos"]
                    else:
                        pos = None
                    ner = mention["ner"]
                    head_word = self.tree_utils.get_constituent_head_word(mention)
                    if head_word:
                        head_word_form = head_word["form"]
                        pos = head_word["pos"]
                    else:
                        error_message = True
                        head_word_form = mention["form"]
                        pos = ""

                    mention["gender"] = self.gender_extractor.get_gender(
                        head_form=head_word_form, pos=pos)
                    mention["number"] = self.gender_extractor.get_number(
                        head_form=head_word_form, pos=pos, ner=ner)
                    mention["animacy"] = self.gender_extractor.get_animacy(
                        head_form=head_word_form, pos=pos, ner=ner)
                    progress_bar.update(index + 1)
                    # Send a warning if not all head found

                    out.write(" # ".join((mention["form"],
                                          str(mention["span"][0] - 1),
                                          str(mention["span"][1]),
                                          head_word_form, mention["gender"], mention["number"], mention["animacy"], "\n")))
                progress_bar.finish()
            if error_message:
                sys.stderr.write("WARNING NO HEAD FOUND without heads strict head match and pronoun sieve will not" +
                                 " work correctly\n")
            self.CP.resolve_text()
            self.graph_builder.statistics_document_up()

        else:
            sys.stderr.write("No mention founds. Check language selected.")

    def show_graph(self):
        """Show the graph in graphviz screen"""
        self.graph_builder.show_graph()

    def process_text(self, original_text):
        self.reset_graph()
        self.build_graph(original_text)
        self.post_process_document()

    ## def store_analysis(self, encoding, language, version, lp_name, lp_version, lp_layer, ):
    ##     """ Stores a corpus analysis results into files.
    ##     """
    ##     writer = KafDocument(stream=sys.stdout)
    ##     writer.store(self.graph, encoding=encoding, language=language, version=version, linguistic_parsers=[
    ##         (lp_name, lp_version, lp_layer)])

    def store_analysis(self, encoding, language, version, lp_name, lp_version, lp_layer, timestamp, ):
        """ Stores a corpus analysis results into files.
        """
        writer = KafDocument(stream=sys.stdout)
        writer.store(self.graph, encoding=encoding, language=language, version=version, linguistic_parsers=[
            (lp_name, lp_version, lp_layer, timestamp)])


    def clean_treebank(self, treebank_file):
        """Remove from treebank file all spurious character."""
        treebank_file = treebank_file.strip()
        return treebank_file

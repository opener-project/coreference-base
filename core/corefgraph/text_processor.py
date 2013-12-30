# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from .features.grendel import GenderNumberExtractor
from .features.speakerExtractor import SpeakerExtractor
from .graph.kafx import KafAndTreeGraphBuilder
from .multisieve.core import CoreferenceProcessor
from .output.progressbar import Fraction, ProgressBar

import logging


class TextProcessor:
    """ Process a single text or corpus with several NLP stages managing the result as graphs.
    """

    def __init__(self, verbose, reader, lang, sieves, sieves_options, extractor_options, singleton,
                 logger=logging.getLogger("arquitecture")):
        self.verbose = verbose
        self.logger = logger
        self.logger.debug("Options %s", sieves_options)
        self.lang = lang
        self.sieves = sieves
        self.sieves_options = sieves_options
        self.extractor_options = extractor_options
        # Graph builder and manager
        self.graph = None
        self.graph_builder = KafAndTreeGraphBuilder(reader)
        self.gender_extractor = GenderNumberExtractor(
            probabilistic_gender=GenderNumberExtractor.use_probabilistic_gender_classification in extractor_options)
        #literator =  SpeakerExtractor(graph=self.graph, graph_builder=self.graph_builder)
        self.speaker_extractor = SpeakerExtractor(graph=self.graph, graph_builder=self.graph_builder).extract
        #self.speech_extractor = literator.speech_extractor
        self.singleton = singleton
        self.tree_utils = None
        self.coreference_processor = None

    def reset_graph(self):
        """Reset the graph and the elements that used a graph reference.

        """
        # Graph attributes
        graph = self.graph_builder.new_graph()
        self.graph = graph
        self.graph_builder.set_graph(graph)
        self.tree_utils = self.graph_builder.get_graph_utils()
        self.coreference_processor = CoreferenceProcessor(
            graph=graph, lang=self.lang, sieves_list=self.sieves, sieves_options=self.sieves_options,
            extractor_options=self.extractor_options, singletons=self.singleton,
            logger=self.logger, verbose=self.verbose)

    def build_graph(self, document):
        """Build a graph form external parser.

        @param document: The document to generate the graph.
        """
        self.graph_builder.process_document(graph=self.graph, document=document)
        sentences_parsed = self.graph_builder.get_sentences()

        for index, sentence in enumerate(sentences_parsed):
            # Dependency graph construction
            sentence_root = self.graph_builder.process_sentence(
                graph=self.graph, sentence=sentence, sentence_namespace="text@{0}".format(index), root_index=index)
            # Generate Coreference Candidatures for the sentence
            self.coreference_processor.process_sentence(sentence_root)

    def post_process_document(self):
        """ Prepare the graph for output.
        """
        error_message = False
        candidatures = self.coreference_processor.get_candidates()
        if len(candidatures):
            if self.verbose:
                widgets = ['Setting gender ', Fraction()]
                progress_bar = ProgressBar(widgets=widgets, maxval=len(candidatures) or 1, force_update=True).start()

            for index, entity in enumerate(candidatures):
                # The entities are singletons yet
                mention = self.graph.node[entity[0]]
                ner = self.graph_builder.get_ner(mention)
                head_word = self.graph_builder.get_head_word(mention)
                if head_word:
                    head_word_form = head_word["form"]
                    pos = head_word["pos"]
                else:
                    error_message = True
                    head_word_form = mention["form"]
                    pos = mention["pos"]

                if self.tree_utils.is_enumeration(mention):
                    mention["number"] = self.gender_extractor.PLURAL
                    mention["gender"] = self.gender_extractor.UNKNOWN
                else:
                    mention["gender"] = self.gender_extractor.get_gender(
                        word_form=head_word_form, word_pos=pos)
                    mention["number"] = self.gender_extractor.get_number(
                        word_form=head_word_form, word_pos=pos, word_ner=ner)
                mention["animacy"] = self.gender_extractor.get_animacy(
                    word_form=head_word_form, word_pos=pos, word_ner=ner)
                mention["speaker"] = self.speaker_extractor(mention, head_word)

                if type(mention["speaker"]) is dict:
                    mention["speaker"]["is_speaker"] = True
                if self.verbose:
                    progress_bar.update(index + 1)
                # Send a warning if not all head found
                self.logger.debug(
                    " # ".join((mention["form"],
                    str(mention["span"][0] - 1), str(mention["span"][1]),
                    head_word_form, mention["gender"], mention["number"], mention["animacy"], "\n")))
            if self.verbose:
                progress_bar.finish()
            if error_message:
                self.logger.warning("WARNING NO HEAD FOUND without heads strict head match and pronoun sieve will not\
                                  work correctly\n")
            self.coreference_processor.resolve_text()
            self.graph_builder.statistics_document_up()

        else:
            self.logger.warning("No mention founds. Check language selected.\n")

    def show_graph(self):
        """Show the graph in screen"""
        self.graph_builder.show_graph()

    def process_text(self, document):
        """ Generate a graph with all linguistic info from de document, resolve the coreference and output the results.

        @param document:
        """
        self.reset_graph()
        self.build_graph(document)
        self.post_process_document()

    def store_analysis_kaf(self, stream, encoding, language, version, lp_name, lp_version, lp_layer, time_stamp ):
        """ Stores a corpus analysis results into files.
        """
        from .output.kafwritter import KafDocument
        writer = KafDocument(stream=stream)
        writer.store(self.graph, encoding=encoding, language=language, version=version, linguistic_parsers=[
            (lp_name, lp_version, lp_layer)], time_stamp=time_stamp)

    def store_analysis_naf(self, stream, encoding, language, version, lp_name, lp_version, lp_layer, time_stamp ):
        """ Stores a corpus analysis results into files.
        """
        from .output.nafwritter import KafDocument
        writer = KafDocument(stream=stream)
        writer.store(self.graph, encoding=encoding, language=language, version=version, linguistic_parsers=[
            (lp_name, lp_version, lp_layer)], time_stamp=time_stamp)

    def store_analysis_conll(self, stream, document_id, part_id):
        """ Stores a corpus analysis results into conll files.
        """
        from .output.conllwriter import ConllDocument
        writer = ConllDocument(stream=stream)
        writer.store(self.graph, document_id, part_id)

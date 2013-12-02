# coding=utf-8
""" This module contains the primary infrastructure and the entry point class for usage the module.
"""
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '14-11-2012'


from ..multisieve.mentionSelection import SentenceCandidateExtractor
from ..output.progressbar import ProgressBar, Fraction
from . import sieves

import logging


class MultiSieveProcessor():
    """A coreference detector based on the lee et all. 2013 multi sieve system of Stanford University.
    """

    def __init__(self, graph, lang_code, sieves_list, sieves_options):
        if not sieves_list or len(sieves_list) < 0:
            sieves_list = sieves.default
        if "NO" in sieves_list:
            sieves_list = []
        self.graph = graph
        self.lang_code = lang_code.lower()
        self.sieves_instances = [sieves.sieves[sieve_class](self, sieves_options)
                                 for sieve_class in sieves_list]

    def process(self, clusters, candidates_per_mention, registers):
        """ Process a candidate cluster list thought the sieves using the output of the each sieve as input of the next.
        :param clusters: The list of mentions.
        :param candidates_per_mention: a dictionary of candidates per mention
        :param registers: The register of each cluster.
        """
        sieve_input = clusters
        for sieve in self.sieves_instances:
            sieve_input = sieve.resolve(sieve_input, candidates_per_mention, registers)
        return sieve_input


class CoreferenceProcessor:
    """ Detect chunks or word of a graph as coreferent with each others.
    """

    def __init__(self, graph, lang,
                 sieves_list, sieves_options,
                 extractor_options, singletons, logger=logging.getLogger("sieves"), verbose=False):
        self.verbose = verbose
        self.logger = logger

        self.singletons = singletons
        self.graph_builder = graph.graph["graph_builder"]
        self.graph_utils = graph.graph["utils"]
        self.graph = graph

        self.candidate_extractor = SentenceCandidateExtractor(
            graph=graph, graph_builder=self.graph_builder, options=extractor_options)
        self.multi_sieve = MultiSieveProcessor(graph, lang, sieves_list, sieves_options)
        self.mentions_textual_order = []
        self.mention_clusters = []
        self.register = list()
        self.candidates_per_mention = dict()

    def get_clusters(self):
        """ Return the list of mention clusters and their candidates.
        """
        return self.mention_clusters

    def get_candidates(self):
        """ Get the candidates extracted by the system.
        @return:
        """
        return self.mention_clusters

    def add_candidatures(self, constituent_order, text_order):
        """ Add to the candidatures list all the mentions in textual order. Also creates a list of candidates for each
        mention based en constituent_order for their sentence mentions add then all others mentions in text order.
        :param constituent_order: The constituent ordered
        :param text_order: The sentence mentions in text appearance order.
        """
        for mention in text_order:
            candidates = []
            # Add the candidates of the sentence until find the constituent of the mention then:
            for mention_list in constituent_order:
                if mention in mention_list:
                    candidates = mention_list[:mention_list.index(mention)] + candidates
                    break
                else:
                    candidates += mention_list

            # Put these constituent candidates in first place and add previous sentences candidates in textual order
            candidates += self.mentions_textual_order
            self.mention_clusters.append([mention])
            self.candidates_per_mention[mention] = candidates
            self.register.append(mention + "orig")
        self.mentions_textual_order.extend(text_order)

    def process_sentence(self, sentence):
        """ Fetch the sentence mentions and generate candidates for they.
        :param sentence: The sentence syntactic tree root node.
        """
        # Extract the mentions
        mentions_bft, mentions_text_order, mentions_constituent_order = self.candidate_extractor.process_sentence(
            sentence=sentence)
        # Add new clusters and candidates
        # self.add_candidatures(mentions_bft, mentions_text_order)
        self.add_candidatures(mentions_constituent_order, mentions_text_order)

    def resolve_text(self):
        """ For a candidate marked graph, resolve the coreference.
        """
        singletons = self.singletons
        verbose = self.verbose
        indexed_clusters = 0
        # Pass the sieves to resolve the coreference
        coreference_proposal = self.multi_sieve.process(
            self.mention_clusters, self.candidates_per_mention, self.register)
        # Logging
        progress_bar = None
        if verbose:
            widgets = ['Indexing clusters', Fraction()]
            progress_bar = ProgressBar(
                widgets=widgets, maxval=len(coreference_proposal) or 1, force_update=True).start()
        # From the coreference cluster add the acceptable result to the graph
        for index, entity in enumerate(coreference_proposal):
            if verbose:
                progress_bar.update(index + 1)
            # Remove the singletons
            mentions = []
            for mention_id in entity:
                unfiltered_mention = self.graph.node[mention_id]
                if not self.purge(unfiltered_mention):
                    mentions.append(unfiltered_mention)
            if singletons or len(mentions) > 1:
                # Add the entity
                self.graph_builder.add_entity(
                    entity_id="EN{0}".format(index), mentions=entity, label=self.register[index])
                indexed_clusters += 1
        # Log the accepted clusters
        if self.verbose:
            progress_bar.finish()
        self.logger.info("Indexed clusters: %d", indexed_clusters)

    @staticmethod
    def purge(mention):
        """ Check if the mention is marked to purge.
        @param mention: A mention to be tested
        @return: True or False
        """
        return mention.get("purge", False)

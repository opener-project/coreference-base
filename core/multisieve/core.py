import logging
from multisieve.mentionSelection import SentenceCandidateExtractor
from multisieve.sieves.exactMatch import ExactMatch
from multisieve.sieves.preciseConstruct import RoleAppositiveConstruction, AcronymMatch, RelativePronoun, \
    PredicativeNominativeConstruction, AppositiveConstruction
from multisieve.sieves.pronoumMatch import PronounMatch
from output.progressbar import ProgressBar, Fraction
from graph.utils import GraphWrapper
from multisieve.sieves.strictHeadMatching import StrictHeadMatching

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '14-11-2012'


class MultiSieveProcessor():
    """A coreference detector based on the lee et all. 2013 multi sieve system of Stanford University.
    """

    sieves_configurations = {"base": [ExactMatch],
                             "full": [ExactMatch, RoleAppositiveConstruction, StrictHeadMatching,  AcronymMatch, AppositiveConstruction,
                                      RelativePronoun, PredicativeNominativeConstruction, PronounMatch,

                                      ]}

    def __init__(self, graph, lang_code, sieves_configuration="full"):
        self.graph = graph
        self.lang_code = lang_code.lower()
        self.sieves_instances = [sieve_class(self) for sieve_class in self.sieves_configurations[sieves_configuration]]

    def process(self, candidatures):
        """ Process a candidate cluster list thought the sieves using the output of the each sieve as input of the next.
        :param candidatures: The list of mentions and their candidates.
        """
        sieve_input = candidatures
        for sieve in self.sieves_instances:
            sieve_input = sieve.resolve(sieve_input)
        return sieve_input


class CoreferenceProcessor:
    """ Detect chunks or word of a graph as coreferent with each others.
    """

    def __init__(self, graph, graph_builder, singletons, logger=logging.getLogger("Coreference Resolver"),
                 verbose=False):
        self.verbose = verbose
        self.logger = logger
        self.graph = graph
        self.singletons = singletons
        self.graph_builder = graph_builder
        self.syntax_graph = self.graph_builder.get_syntax_graph(graph)

        self.candidate_sentence = SentenceCandidateExtractor(graph=self.graph, constituent=True)
        self.multi_sieve = MultiSieveProcessor(self.graph, "en")
        self.old_sentences = []
        self.old_sentences_pronominal = []
        self.candidatures = []

    def get_clusters(self):
        """ Return the list of mention clusters and their candidates.
        """
        return self.candidatures

    def get_candidates(self):
        return self.candidatures

    def process_sentence(self, sentence_root):
        """ Fetch the sentence mentions and generate candidates for they.

        :param sentence_root: The sentence syntactic tree root node.
        """
        sentence_candidatures, candidates = self.candidate_sentence.process_sentence(
            sentence=sentence_root,
            previous_sentences_candidates=self.old_sentences)
        self.old_sentences = candidates + self.old_sentences
        self.candidatures.extend(sentence_candidatures)

    def sieves_register(self):
        """ For a candidate marked graph, resolve the coreference.
        """
        # The property that mark coreference in words
        word_coreference = GraphWrapper.node_property("coreference", self.graph)
        self.coreference_proposal = self.multi_sieve.process(self.candidatures)
        # For each custer assign a zero based index as id
        widgets = ['Indexing clusters', Fraction()]
        pbar = ProgressBar(widgets=widgets, maxval=len(self.coreference_proposal), force_update=True).start()
        indexed_clusters = 0
        #TODO gestionar los singletons desde el output
        for index, (entity, candidates, sieves_register) in enumerate(self.coreference_proposal):
            pbar.update(index + 1)
            # Remove the singletons
            if len(entity) > 1 or self.singletons:
                self.graph_builder.add_entity(mentions=entity, label=sieves_register)
                #TODO test if the next code is useful
                indexed_clusters += 1
                for mention in entity:
                    # For each mention word assign the cluster id to cluster attribute
                    # and mark start and end with '(' and ')'
                    tokens = self.graph_builder.get_constituent_words(mention)
                    # Valid for 0, 1 and n list sides
                    if tokens:
                        if len(tokens) == 1:
                            word_coreference[tokens[0]].append("({0})".format(index))
                        else:
                            word_coreference[tokens[0]].append("({0}".format(index))
                            word_coreference[tokens[-1]].append("{0})".format(index))
                            #for token in tokens[1:-1]:
                            #    word_coreference[token] .append( str_index)
        self.logger.info("Indexed clusters: %d", indexed_clusters)

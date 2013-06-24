import logging
from multisieve.mentionSelection import SentenceCandidateExtractor
from multisieve.sieves.exactMatch import ExactMatch
from multisieve.sieves.preciseConstruct import RoleAppositiveConstruction, AcronymMatch, RelativePronoun, \
    PredicativeNominativeConstruction, AppositiveConstruction
from multisieve.sieves.pronoumMatch import PronounMatch
from output.progressbar import ProgressBar, Fraction
from graph.xutils import GraphWrapper
from multisieve.sieves.strictHeadMatching import StrictHeadMatching

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '14-11-2012'


class MultiSieveProcessor():
    """A coreference detector based on the lee et all. 2013 multi sieve system of Stanford University.
    """

    sieves_configurations = {"base": [ExactMatch],
                             "full": [ExactMatch, AppositiveConstruction, RoleAppositiveConstruction, StrictHeadMatching,  AcronymMatch,
                                      RelativePronoun, PredicativeNominativeConstruction, PronounMatch,
                                      ],
                             "dev": [ExactMatch, AppositiveConstruction, RoleAppositiveConstruction, PredicativeNominativeConstruction,
                                     RelativePronoun, StrictHeadMatching, AcronymMatch, # PronounMatch,
                                     ]
    }
    ### LOOK OUT!!!
    def __init__(self, graph, lang_code, sieves_configuration="full"):
        self.graph = graph
        self.lang_code = lang_code.lower()
        self.sieves_instances = [sieve_class(self) for sieve_class in self.sieves_configurations[sieves_configuration]]

    def process(self, clusters, candidates_per_mention, registers):
        """ Process a candidate cluster list thought the sieves using the output of the each sieve as input of the next.
        :param clusters: The list of mentions and their candidates.
        """
        sieve_input = clusters
        for sieve in self.sieves_instances:
            sieve_input = sieve.resolve(sieve_input, candidates_per_mention, registers)
        return sieve_input


class CoreferenceProcessor:
    """ Detect chunks or word of a graph as coreferent with each others.
    """

    def __init__(self, graph, singletons, logger=logging.getLogger("Coreference Resolver"),
                 verbose=False):
        self.verbose = verbose
        self.logger = logger
        #self.graph = graph
        self.singletons = singletons
        self.graph_builder = graph.graph["graph_builder"]

        self.candidate_extractor = SentenceCandidateExtractor(graph=graph)
        self.multi_sieve = MultiSieveProcessor(graph, "en")
        self.mentions_textual_order = []
        self.mention_clusters = []
        self.register = list()
        self.candidates_per_mention = dict()

    def get_clusters(self):
        """ Return the list of mention clusters and their candidates.
        """
        return self.mention_clusters

    def get_candidates(self):
        return self.mention_clusters

    def add_candidatures(self, bsft_order, text_order):
        """ Add to the candidatures list All the mentions in textual order.
        :param bsft_order: The sentence mentions in bft per sentence constituent.
        :param text_order: The sentence mentions in text appearance order .
        """
        for mention in text_order:
            index = bsft_order.index(mention)
            candidates = bsft_order[:index] + self.mentions_textual_order
            self.mention_clusters.append([mention])
            self.candidates_per_mention[mention] = candidates
            self.register.append(mention + "orig")
        self.mentions_textual_order.extend(text_order)

    def process_sentence(self, sentence_root):
        """ Fetch the sentence mentions and generate candidates for they.
        :param sentence_root: The sentence syntactic tree root node.
        """
        # Extract the mentions
        mentions_bsft, mentions_text_order = self.candidate_extractor.process_sentence(
            sentence=sentence_root)
        # Add new clusters and candidates
        self.add_candidatures(mentions_bsft, mentions_text_order)

    def resolve_text(self):
        """ For a candidate marked graph, resolve the coreference.
        """
        # Logging
        widgets = ['Indexing clusters', Fraction()]
        indexed_clusters = 0
        # Pass the sieves to resolve the correference
        coreference_proposal = self.multi_sieve.process(self.mention_clusters, self.candidates_per_mention, self.register)
        # More log
        pbar = ProgressBar(widgets=widgets, maxval=len(coreference_proposal) or 1, force_update=True).start()
        # From the correference cluster add the acceptable result to the graph
        for index, entity in enumerate(self.mention_clusters):
            pbar.update(index + 1)
            # Remove the singletons
            if len(entity) > 1 or self.singletons:
                # Add the entity
                self.graph_builder.add_entity(
                    entity_id="EN{0}".format(index), mentions=entity, label=self.register[index])
                indexed_clusters += 1
        # Log the accepted clusters
        self.logger.info("Indexed clusters: %d", indexed_clusters)

from graph.utils import GraphWrapper
from multisieve import dictionaries
from multisieve.syntatic_tree_utils import SyntacticTreeUtils

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class SentenceCandidateExtractor:
    """ Extract the candidates of a sentence
    """
    valid_mention_phrase = ("NP", "WHNP")
    pronoun_pos = ("PRP", "PRP$")
    proper_pos = ("NNP", "NNPS")
    valid_NER = ("PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART",
                 "LAW", "LANGUAGE", "DATE", "TIME")
    invalid_ner = ("PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")
    non_words = "mm", "hmm", "ahem", "um"
    invalid_stop_words = {"there", "ltd.", "etc", "'s", "hmm"}

    indefinite_start_particles = set()
    indefinite_start_particles.update(dictionaries.indefinite_pronouns)
    indefinite_start_particles.update(dictionaries.indefinite_articles)

    nominal_mention = "nominal_mention"
    proper_mention = "proper_mention"
    pronoun_mention = "pronoun_mention"
    indefinite_mention = "undefined_mention"
    no_mention = "no_mention"

    def __init__(self, graph, reverse=False, constituent=False, order_property="ord"):
        self.constituent = constituent
        self.reverse = reverse
        self.order_property = order_property

        self.graph = graph

        GraphWrapper.define_properties(graph=self.graph, vertex_properties={"mention_type": "string"})

        self.graph_builder = GraphWrapper.get_graph_property(graph=graph, property_name="graph_builder")
        self.tree_utils = SyntacticTreeUtils(self.graph)

        self.node_mention_type = GraphWrapper.node_property(name="mention_type", graph=graph)
        self.node_form = GraphWrapper.node_property(name="form", graph=graph)
        self.node_pos = GraphWrapper.node_property(name="pos", graph=graph)
        self.node_ner = GraphWrapper.node_property(name="ner", graph=graph)
        self.node_type = GraphWrapper.node_property(name="type", graph=graph)
        self.node_tag = GraphWrapper.node_property(name="tag", graph=graph)
        self.node_lemma = GraphWrapper.node_property(name="lemma", graph=graph)
        self.node_head = GraphWrapper.node_property(name="head", graph=graph)
        self.node_ord = GraphWrapper.node_property(name="ord", graph=graph)

        self.syntactic_node_type = self.graph_builder.syntactic_node_type
        self.syntactic_edge_type = self.graph_builder.syntactic_edge_type

    def get_syntactic_parent(self, node):
        """Return the syntactic parent of the chunk
        :param node: The node chunk or word whose parent is wanted.
        """
        parents = GraphWrapper.get_filtered_by_type_in_neighbours(node=node, relation_type=self.syntactic_edge_type)
        if parents:
            return parents[0]
        return None

    def get_syntactic_children(self, chunk):
        """Get the list of the syntactic children of the chunk
        :param chunk: The chunk whose children of syntactic tree (chunk or word) are wanted.
        """
        return GraphWrapper.get_filtered_by_type_out_neighbours(node=chunk, relation_type=self.syntactic_edge_type)

    def validate_node(self, mention_candidate, filter_candidates=True):
        """Determine if a node is a valid mention.
        :param filter_candidates: The candidate once is determided from a valid source(NP,PRP,NER) is filtered?
        :param mention_candidate: The candidate Node (Word or chunk) to be validates as mention.
        """
        # Pass filters
        first_filter = False
        # its a chunk
        if self.node_type[mention_candidate] == self.syntactic_node_type:
            # It's a NP or WHNP
            if self.node_tag[mention_candidate].upper() in self.valid_mention_phrase:
                first_filter = True

        # It's a pronoun
        elif self.node_pos[mention_candidate].upper() in self.pronoun_pos :
            first_filter = True
        # Wathever, It's a valid NER?
        ner = self.node_ner[mention_candidate].upper()
        if ner in self.valid_NER:
            first_filter = True

        # Is a plausible Mention?
        if not first_filter:
            return False
            # Refine the mentions?
        if not filter_candidates:
            return True

        # Useful characteristic
        candidate_form = self.node_form[mention_candidate]
        parent = self.get_syntactic_parent(mention_candidate)

        # remove mentions that are numeric entities
        if ner in self.invalid_ner:
            return False
        # remove mentions with partitive or quantifier expressions
        if candidate_form.split()[0] in dictionaries.quantifiers:
            return False
        #TODO Improve lone "of" filtering
        if 'of' in candidate_form and len(candidate_form) > 2:
            words = candidate_form.split("of")
            if words[0].split()[-1].strip() in dictionaries.partitives:
                return False
            # Remove pleonastic "it" pronouns
        #TODO Pleonastic it
        # Remove adjectival forms of nations or nationality acronyms
        if candidate_form in dictionaries.demonyms:
            return False
            #TODO Nationality acronyms
        # Remove stop words
        if candidate_form in self.invalid_stop_words:
            return False

        # remove mentions that have a larger version
        head = self.graph_builder.get_chunk_head(mention_candidate) or mention_candidate
        # If the head of the mention is a word and the word is in a bigger mention isn't a valid mention
        if self.node_type[head] == self.graph_builder.word_node_type and \
                not self.tree_utils.is_appositive_construction(mention_candidate):
            childrend_pos = set([self.node_pos[child] for child in self.graph_builder.get_chunk_children(mention_candidate)])
            # If all children are NNP or NNPS the head is the chunk not a terminal word
            if self.node_type[mention_candidate] == self.graph_builder.word_node_type or \
                    len(childrend_pos - set(("NNP", "NNPS"))):
                higher_chunk = parent
                higher_chunk_head = self.graph_builder.get_chunk_head(parent)
                while higher_chunk:
                    if self.node_mention_type[higher_chunk] and self.node_mention_type[higher_chunk] != self.no_mention\
                            and higher_chunk_head and self.node_form[head] in self.node_form[higher_chunk_head]:
                        return False
                    higher_chunk = self.get_syntactic_parent(higher_chunk)
        #print node_form,  self.node_type[mention_candidate]
        return True

    def set_mention_type(self, node, mention_type):
        """ The node is set as a mention of the specify type.
        :param node: The node to be set as mention.
        :param mention_type: The mention type used to set the node.
        """
        self.node_mention_type[node] = mention_type

    def select_mention_type(self, mention, ordered_children):
        head = None
        if self.node_type[mention] == self.graph_builder.word_node_type:
            head = mention
        else:
            for child in ordered_children:
            # Head Child determines mention type
                if self.node_head[child]:
                    head = child
                    break
        # Pronoun mention
        if head and self.node_pos[head] in self.pronoun_pos:
            return self.pronoun_mention
        # Indefinite Mention
        if len(ordered_children) and (self.node_form[ordered_children[0]] in self.indefinite_start_particles):
            return self.indefinite_mention
        # In other case is nominal
        return self.nominal_mention

    def order_constituent(self, root, previous_candidates):
        """ Order the sentence syntax nodes in filtered breath-first-transverse.
        :param root: The root of the sentence syntactic tree.
        :param previous_candidates: The candidates from previous sentences. Used to attach to founded mentions as
        candidates.
        """
        # The ordered nodes of the constituent tha can be candidates
        candidates = []
        nodes = [self.syntax_graph.vertex(root)]
        visited = []
        candidatures = []
        # Process all the nodes
        while nodes:
            # Extract the first candidate
            node = nodes.pop(0)
            visited.append(node)
            if  self.node_tag[node].startswith("S"):
                clause_candidatures, clause_candidates = self.process_S_chunk(node, candidates + previous_candidates)
                candidates.extend(clause_candidates)
                candidatures.extend(clause_candidatures)
            else:
                # Order the children of the nodes
                ordered_children = sorted(GraphWrapper.get_filtered_by_type_out_neighbours(node, "syntactic"),
                                          key=lambda child: self.node_ord[child], reverse=self.reverse)
                # Assign a index if the node is candidate for indexing
                if self.validate_node(node):
                    # Node is a mention
                    # TODO store the textual order of node
                    # Determine de mention type
                    mention_type = self.select_mention_type(node, ordered_children)

                    self.set_mention_type(node, mention_type)
                    # store an candidature of the current constituent candidates and older constituent
                    candidatures.append(([self.graph.vertex(node)], [candidates + previous_candidates],
                                         ["orig:{0}".format(self.node_form[node])]))
                    # Add current node as candidate for the next mentions
                    candidates.append(self.graph.vertex(node))
                else:
                    ordered_children = sorted(GraphWrapper.get_filtered_by_type_out_neighbours(node, "syntactic"),
                                              key=lambda child: self.node_ord[child], reverse=self.reverse)
                    # Node is not a mention
                    self.node_mention_type[node] = self.no_mention
                nodes.extend(ordered_children)
        # Return the candidatures and the candidates for next constituent candidatures
        return candidatures, candidates

    def skip_root(self, sentence_root):
        """Get the first chunk of the sentence (usually S) Skip al ROOT nodes,created by the parser o the graph builder.
        Skip all the dummy roots crated by the parsers/graph builder.
        :param sentence_root: The syntactic tree root node.
        """
        #    return next(next(sentence_root.out_neighbours()).out_neighbours())
        chunk = sentence_root
        while chunk and (self.node_tag[chunk] == self.graph_builder.root_pos):
            chunk = next(chunk.out_neighbours())
        return chunk

    def process_S_chunk(self, s_chunk, previous_candidates):
        sentence_candidatures = []
        sentence_candidates = []
        # Visit each constituent in a BFT algorithm
        ordered_constituents = sorted(s_chunk.out_neighbours(),
                                      key=lambda child: self.node_ord[child])
        for constituent in ordered_constituents:
            # generate  order candidates in this form:
            #   this_constituent candidates + other constituent candidates_in_LtR + other_sentence_candidates
            (constituent_candidatures, constituent_candidates) = self.order_constituent(
                constituent, sentence_candidates + previous_candidates, )
            # The last constituent is in right place of the sentence
            # so its candidates are put at last of the list
            sentence_candidates.extend(constituent_candidates)
            sentence_candidatures.extend(constituent_candidatures)
        return sentence_candidatures, sentence_candidates + previous_candidates

    def process_sentence(self, sentence, previous_sentences_candidates):
        """ Order all graph syntactic trees in filtered breath-first-transverse.
        :param previous_sentences_candidates: Candidates form previous sentences used for attach to mentions as
        candidates.
        :param sentence: The sentence whose mentions are wanted.
        """
        # Get al the syntax trees trees in order of appear
        # Get a Graph that only contains syntax edges
        self.syntax_graph = self.graph_builder.get_syntax_graph(graph=self.graph)
        syntax_root = self.skip_root(self.syntax_graph.vertex(sentence))

        return self.process_S_chunk(s_chunk=syntax_root, previous_candidates=previous_sentences_candidates)
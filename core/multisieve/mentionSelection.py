# coding=utf-8
""" Module that contains all necessary stuff to detect the mentions present in a sentence and supply a ordered list of
 candidates for each mention.

"""
from graph.kafx import SyntacticTreeUtils

from resources.tagset import pos_tags, constituent_tags, ner_tags
from resources.dictionaries import stopwords, determiners
from resources.demonym import demonyms

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class SentenceCandidateExtractor:
    """ Extract all the mentions of a text. The text if analysed sentence by sentence,
    """

    nominal_mention = "nominal_mention"
    proper_mention = "proper_mention"
    pronoun_mention = "pronoun_mention"
    indefinite_mention = "undefined_mention"
    #no_mention = "no_mention"

    def __init__(self, graph, order_property="ord"):

        self.order_property = order_property
        self.graph = graph
        self.tree_utils = SyntacticTreeUtils(self.graph)


    def _inside_ne(self, mention_span):
        """check if a span is inside any Named entity span of the current sentence and is not the entity.

        :param span_x: The start of the span(in token counts).
        :param span_y: The end of the span(in token counts)."""
        for entity_span in self.named_entities_span:
            if self.tree_utils.inside(mention_span, entity_span) and not mention_span == entity_span:
                return True
        return False

    def validate_node(self, mention_candidate):
        """Determine if a node is a valid mention.
        :param mention_candidate: The candidate Node (Word or chunk) to be validates as mention.
        """
        # Actually is a trigger to insert named entities in their correct place
        if mention_candidate["id"] in self.named_entities_by_constituent:
            # Silently insert the Named entity and fails mention
            named_entity_mention = self.named_entities_by_constituent.pop(mention_candidate["id"])
            self.add_mention(named_entity_mention)
            return False
        #TODO May this not have to null the constituent check

        span = mention_candidate["span"]
        if span in self.candidates_span or self._inside_ne(span):
            return False

        # Pass filters
        first_filter = False
        # it's a pronoun
        if "pos" in mention_candidate and pos_tags.personal_pronouns(mention_candidate["pos"]):
            first_filter = True

        # it's a Valid constituent
        elif "tag"in mention_candidate and \
                constituent_tags.mention_constituents(mention_candidate["tag"]):
            first_filter = True

        # it's part of a enumeration
        #TODO Check if this have to be promoted to first check
        elif ("pos" in mention_candidate and pos_tags.enumerable_mention_words(mention_candidate["pos"])) or\
                ("tag"in mention_candidate and constituent_tags.noun_phrases(mention_candidate["tag"])):
            mention_candidate_parent = self.tree_utils.get_syntactic_parent(mention_candidate)
            if "tag" in mention_candidate_parent and constituent_tags.noun_phrases(mention_candidate_parent["tag"]):
                siblings = self.tree_utils.get_syntactic_sibling(mention_candidate)
                # Search if the next brothers are suitable list candidates
                next_siblings = siblings[siblings.index(mention_candidate):]
                # If a coma or a conjunction if found search for a enumerable
                for index, brother in enumerate(next_siblings):
                    if "pos" in brother and (pos_tags.conjunction(brother["pos"]) or brother["pos"] == ","):
                        for brother in next_siblings[index:]:
                            if ("pos" in brother and pos_tags.enumerable_mention_words(brother["pos"])) or\
                                    ("tag"in brother and constituent_tags.noun_phrases(brother["tag"])):
                                return True

        # Is a plausible Mention?
        if not first_filter:
            return False
        # Refine the mentions?
        form = mention_candidate["form"]

        # TODO Pleonastic it

        # Remove mentions that contains non-words
        if constituent_tags.mention_constituents(form) in stopwords.non_words:
            return False

        # Remove mentions that starts with quantifiers
        # candidate_form = self.node_form[mention_candidate]
        if determiners.quantifiers(form.split()[0]):
            return False

        # Remove mentions that are in a partitive expression: One of then
        sentence_words = self.tree_utils.get_sentence_words(mention_candidate["root"])
        sentence_span = mention_candidate["root"]["span"]
        relative_span = (span[0] - sentence_span[0], span[1] - sentence_span[1])

        if (relative_span[0]-2 > 0) and determiners.partitive_particle(sentence_words[relative_span[0]-1]["form"]) and \
                determiners.partitives(sentence_words[relative_span[0]-2]["form"]):
            return False

        head_word = self.tree_utils.get_constituent_head_word(mention_candidate)

        # Remove candidates with a temporal noun as head
        if pos_tags.singular_noun(head_word["pos"]) and head_word["form"] in stopwords.temporals:
            return False
        self.candidates_span.append(span)

        # Money and perceptual NErs

        if head_word["form"] == "%":
            return False
        if ner_tags.no_mention_ner(head_word["ner"]):
            return False
        # Remove adjectival forms of nations or nationality acronyms(TODO ?)
        if form in demonyms:
            return False
        # Avoid mention if it have the same head word of bigger sentence
        for mention in self.sentence_mentions_bst_order:
            x = 1
            if head_word == mention["head_word"] and self.tree_utils.inside(span, mention["span"]):
                # Check for apposition or enumeration.
                for word in sentence_words[mention["span"][0]:mention["span"][1]]:
                    if pos_tags.conjunction(word["pos"]) or word["form"] == ",":
                        return True
                return False
        return True

    def _set_mention_type(self, node, mention_type):
        """ The node is set as a mention of the specify type.
        :param node: The node to be set as mention.
        :param mention_type: The mention type used to set the node.
        """
        node["mention"] = mention_type
        node["label"] = node["label"] + "\n" + mention_type

    def _select_mention_type(self, mention):
        """ Determine the type of the mention.
        :param mention: The mention to be classified.
        """
        words = self.tree_utils.get_constituent_words(mention)
        head = self.tree_utils.get_constituent_head_word(mention)
        first_pos = words[0]["pos"]
        # Pronoun mention
        if head and pos_tags.mention_pronouns(head["pos"]):
            return self.pronoun_mention
        # Indefinite Mention
        if len(words) and pos_tags.indefinite(first_pos) or determiners.indefinite_articles(first_pos):
            return self.indefinite_mention
        # In other case is nominal
        return self.nominal_mention

    def add_mention(self, mention):
        mention_type = self._select_mention_type(mention)
        mention["head_word"] = self.tree_utils.get_constituent_head_word(mention)
        self.sentence_mentions_bst_order.append(mention)

        self._set_mention_type(mention, mention_type)
        # store an candidature of the current constituent candidates and older constituent

    def extract_mentions_from_constituent(self, root):
        """ Extract mentions from the sentence and generate a candidate list for each mention.
        The constituent syntax graph is traversed in filtered breath-first-transverse order. Each element(constituent or
         word) is evaluated and (if is found valid) added with is coreference candidates to the candidature tuple.

        :param root: The root of the sentence syntactic tree.
        candidates.
        """
        # The ordered nodes of the constituent tha can be candidates

        nodes = [root]
        visited = []

        # Process all the nodes
        while nodes:
            # Extract the first candidate
            node = nodes.pop(0)
            visited.append(node)
            if "tag" in node and constituent_tags.clauses(node["tag"]):
                self._process_constituent_BFST(node)
            else:
                if self.validate_node(node):
                    self.add_mention(node)
                # Order the children of the nodes
                ordered_children = sorted(
                    self.tree_utils.get_constituent_children(node), key=lambda child: child["ord"])
                nodes.extend(ordered_children)

    def _process_constituent_BFST(self, s_chunk):
        """Process each constituent of the chunk in a breath-first-transverse
        :param s_chunk: The chunk where each element must be traversed separately
        """
        # Visit each constituent in a BFT algorithm
        ordered_constituents = sorted(self.tree_utils.get_constituent_children(s_chunk),
                                      key=lambda child: child["ord"])
        for constituent in ordered_constituents:
            self.extract_mentions_from_constituent(constituent)

    def _process_named_entities(self, sentence):
        """Add the named entities to the candidates.

        For every entity in the sentence:
            + Store as a mention
            + Add their span for the no inside NE restriction
         : param sentence: The base node for the sentence named entities. usually the root node.
        """
        for entity in self.tree_utils.get_sentence_named_entities(sentence):
            entity_span = entity["span"]
            # check is not already added
            if entity_span not in self.candidates_span:
                # Alocate in the tree
                constituent = self.tree_utils.allocate_named_entities(entity, sentence)
                # Add the mention to registers
                self.candidates_span.append(entity_span)
                self.named_entities_span.append(entity_span)
                self.named_entities_by_constituent[constituent["id"]] = entity

    def process_sentence(self, sentence):
        """ Extract al the mentions of the Order all graph syntactic trees in filtered breath-first-transverse.

        :param sentence: The sentence whose mentions are wanted.
        """
        self.sentence_mentions_bst_order = []
        self.named_entities_by_constituent = dict()
        # The spans are used to avoid duplicate mentions and mention inside NE
        self.candidates_span = []
        self.named_entities_span = []
        # Prepare the Named entities before the tree traversal
        self._process_named_entities(sentence)
        # Skip useless Root nodes
        syntax_root = self.tree_utils._skip_root(sentence)
        # Thought the rabbit hole
        self._process_constituent_BFST(s_chunk=syntax_root)\
        # Text apearance order
        sentence_mentions_textual_order = [mention["id"] for mention in sorted(self.sentence_mentions_bst_order,
                                                 key=lambda m: m["span"])]
        sentence_mentions_bst_order = [mention["id"] for mention in self.sentence_mentions_bst_order]
        return sentence_mentions_bst_order, sentence_mentions_textual_order
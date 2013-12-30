# coding=utf-8
""" Module that contains all necessary stuff to detect the mentions present in a sentence and supply a ordered list of
 candidates for each mention.

"""

__author__ = 'Josu Bermúdez <josu.bermudez@deusto.es>'


from ..graph.kafx import SyntacticTreeUtils
from ..resources.demonym import demonyms
from ..resources.dictionaries import stopwords, determiners, temporals, pronouns, verbs
from ..resources.tagset import pos_tags, constituent_tags, ner_tags

from collections import defaultdict


class SentenceCandidateExtractor:
    """ Extract all the mentions of a text. The text if analysed sentence by sentence,
    """

    nominal_mention = "nominal_mention"
    proper_mention = "proper_mention"
    pronoun_mention = "pronoun_mention"
    indefinite_mention = "undefined_mention"
    started_by_indefinite = "started_by_undefined_mention"
    #no_mention = "no_mention"

    def __init__(self, graph, graph_builder, options=None, order_property="ord"):
        if options:
            self.filter_same_head_word = not options.no_filter_same_head
        else:
            self.filter_same_head_word = True
        self.filter_same_head_word = True
        self.order_property = order_property
        self.graph = graph
        self.graph_builder = graph_builder
        self.tree_utils = SyntacticTreeUtils(self.graph)
        # List used to keep mention during the tree traversal
        self.sentence_mentions_bft_order = []
        self.sentence_mentions_bft_constituent_order_lists = []
        self.sentence_mentions_bft_constituent_order_current = None
        self.named_entities_by_constituent = defaultdict([].__class__)
        # The spans are used to avoid duplicate mentions and mention inside NE
        self.candidates_span = []
        self.named_entities_span = []

    def _inside_ne(self, mention_span):
        """check if a span is inside any Named entity span of the current sentence and is not the entity.
        """
        for entity_span in self.named_entities_span:
            if self.graph_builder.is_inside(mention_span, entity_span) and not mention_span == entity_span:
                return True
        return False

    def _validate_node(self, mention_candidate):
        """Determine if a node is a valid mention.
        :param mention_candidate: The candidate Node (Word or chunk) to be validates as mention.
        """
        # Actually is a trigger to insert named entities in their correct place
        if mention_candidate["id"] in self.named_entities_by_constituent:
            # Silently insert the Named entity and fails mention
            for named_entity_mention in self.named_entities_by_constituent.pop(mention_candidate["id"]):
                if self._filter_candidate(named_entity_mention, named_entity=True):
                    self._add_mention(named_entity_mention)

        mention_span = mention_candidate["span"]
        mention_pos = mention_candidate.get("pos", "")
        mention_tag = mention_candidate.get("tag", "")

        if mention_span in self.candidates_span or self._inside_ne(mention_span):
            return False

        # Pass filters
        first_filter = False
        # it's a pronoun
        if pos_tags.personal_pronouns(mention_pos) or (mention_candidate["form"] in pronouns.all):
            first_filter = True

        # it's a Valid constituent
        elif constituent_tags.mention_constituents(mention_tag):
            first_filter = True

        # it's part of a enumeration
        #TODO Check if this have to be promoted to first check
        elif pos_tags.enumerable_mention_words(mention_pos)or constituent_tags.noun_phrases(mention_tag):
            mention_candidate_parent = self.graph_builder.get_syntactic_parent(mention_candidate)
            if constituent_tags.noun_phrases(mention_candidate_parent.get("tag", "")):
                # Search if the next brothers are suitable list candidates
                next_siblings = [sibling for sibling in self.graph_builder.get_syntactic_sibling(mention_candidate)
                                 if sibling["span"] > mention_candidate["span"]]
                # If a coma or a conjunction if found search for a enumerable
                for index, brother in enumerate(next_siblings):
                    brother_pos = brother.get("pos", "")
                    if pos_tags.conjunction(brother_pos):
                        # Check if next to comma exist a enumerable sibling
                        for post_comma_brother in next_siblings[index:]:
                            brother_pos = post_comma_brother.get("pos", "")
                            brother_tag = post_comma_brother.get("tag", "")
                            if pos_tags.enumerable_mention_words(brother_pos) or \
                                    constituent_tags.noun_phrases(brother_tag):
                                first_filter = True
        # Is a plausible Mention?
        if not first_filter:
            return False
        # Filter mentions
        result = self._filter_candidate(mention_candidate)
        return result

    def _filter_candidate(self, mention_candidate, named_entity=False):
        """ Check if the mention candidate is valid.

        Remove pleonastic It.
        Remove non-words.
        Remove mentions that starts with quantifiers.
        Remove mentions that are part of partitive expressions.
        Remove
        @param mention_candidate: A plausible mention
        """
        form = mention_candidate["form"].lower()
        span = mention_candidate["span"]
        pos = mention_candidate.get("pos", "None")
        tag = mention_candidate.get("tag", "None")
        head_word = self.graph_builder.get_head_word(mention_candidate)
        head_form = head_word["form"].lower()
        head_word_pos = head_word["pos"]

        # Remove Pleonastic it
        if pos_tags.personal_pronouns(pos) or form in pronouns.all:
            if self.tree_utils.pleonastic_it(mention_candidate):
                return False
                #else:
                #    return True
        # Remove bare NPs
        words = self.graph_builder.get_words(mention_candidate)
        if pos_tags.singular_common_noun(head_word_pos) and \
            head_form not in temporals.temporals and (
                len(words) == 1 or pos_tags.adjectives(words[0]["pos"])):
            return False

        # Remove mentions that contains non-words
        if head_form in stopwords.non_words:
            return False

        # Remove mentions that starts with quantifiers
        if determiners.quantifiers(form.split()[0]):
            return False

        # Remove mentions that are in a partitive expression: One of then
        sentence = self.graph_builder.get_root(mention_candidate)
        sentence_words = self.graph_builder.get_sentence_words(sentence)
        sentence_span = sentence["span"]
        relative_span = (span[0] - sentence_span[0], span[1] - sentence_span[0])

        if (relative_span[0] - 2 > 0) and determiners.partitive_particle(
                sentence_words[relative_span[0] - 1]["form"].lower()) and \
                determiners.partitives(sentence_words[relative_span[0] - 2]["form"].lower()):
            return False

        # Remove candidates with a temporal noun as head
        if head_form in temporals.temporals:
            return False

        # Money and perceptual NEs
        if "%" in head_word["form"]:
            return False
        if ner_tags.no_mention_ner(self.graph_builder.get_ner(mention_candidate)):
            return False
        # Remove interjections
        if pos_tags.interjections(head_word_pos) or constituent_tags.interjections(tag):
            return False
        # Remove adjectival forms of nations or nationality acronyms
        if form in demonyms:
            return False

        # Remove stop words
        if form in stopwords.invalid_stop_words:
            return False
        for start in stopwords.invalid_start_words:
            if form.startswith(start):
                return False
        for start in stopwords.invalid_end_words:
            if form.endswith(start):
                return False

        if not self.filter_same_head_word or named_entity:
            return True
            # Avoid mention if it have the same head word of bigger sentence, except apposition and enumeration.
        for prev_mention in self.sentence_mentions_bft_order:
            prev_head_word = self.graph_builder.get_head_word(prev_mention)
            if head_word["id"] == prev_head_word["id"] and self.graph_builder.is_inside(span, prev_mention["span"]):
                # Check for apposition or enumeration.
                #another_relative_span = (mention["span"][0] - sentence_span[0], mention["span"][1] - sentence_span[0])
                #for word in sentence_words[another_relative_span[0]:another_relative_span[1]]:
                #    if pos_tags.conjunction(word["pos"]) or word["form"] == ",":
                #        return True
                if relative_span[1] + 1 < len(sentence_words):
                    next_word = sentence_words[relative_span[1] + 1]
                    if pos_tags.conjunction(next_word["pos"]):
                        return True
                return False
        return True

    def _set_generics(self, mention):
        """Check and set the mention generic attribute.
        :param mention: The mention to check
        :return:Nothing
        """
        mention["generic"] = False
        head_word = self.graph_builder.get_head_word(mention)
        #Bare plural
        if pos_tags.plural_common_noun(head_word["pos"]) and \
                (mention["span"][1] - mention["span"][0] == 0):
            mention["generic"] = True
        # Generic you as in "you know"
        elif mention["doc_type"] == "conversation" and mention["form"].lower() in pronouns.second_person:
            you = head_word
            sentence = self.graph_builder.get_root(you)
            words = [word["id"] for word in self.graph_builder.get_sentence_words(sentence)]
            you_index = words.index(you["id"])
            if (you_index + 1 < len(words)) and \
                    self.graph.node[words[you_index + 1]]["lemma"].lower() in verbs.generics_you_verbs:
                mention["generic"] = True

    @staticmethod
    def _set_mention_type(node, mention_type):
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
        words = self.graph_builder.get_words(mention)
        head = self.graph_builder.get_head_word(mention)
        head_pos = head["pos"]
        head_form = head["form"].lower()
        head_ner = self.graph_builder.get_ner(head)
        first_pos = words[0]["pos"]
        first_form = words[0]["form"].lower()
        if determiners.indefinite_articles(first_form):
            mention[self.started_by_indefinite] = True
        else:
            mention[self.started_by_indefinite] = False
        # Pronoun mention
        if pos_tags.mention_pronouns(head_pos) or \
                (len(words) == 1 and head_form in pronouns.all and ner_tags.no_mention_ner(head_ner)):
            return self.pronoun_mention
        # Indefinite Mention
        if len(words) > 1 and (
                pos_tags.indefinite(first_pos) or
                determiners.indefinite_articles(first_form)):
            return self.indefinite_mention
        # In other case is nominal
        return self.nominal_mention

    def _add_mention(self, mention):
        """ Add mention to the sentence mention cluster.
        Assign the HeadWord of the mention.
        Set if the mention is generics
        @param mention: A valid and checked mention mention 
        """
        mention_type = self._select_mention_type(mention)

        self._set_generics(mention)
        self._set_appositive(mention)
        self._set_predicative_nominative(mention)
        self._set_mention_type(mention, mention_type)

        self.sentence_mentions_bft_order.append(mention)
        self.sentence_mentions_bft_constituent_order_current.append(mention)
        self.candidates_span.append(mention["span"])
        # store an candidature of the current constituent candidates and older constituent

    def _extract_mentions_from_constituent(self, root):
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
            # Clauses are traversed in same way as roots
            if "tag" in node and constituent_tags.clauses(node["tag"]):
                self._process_constituent_bfst(node)
            else:
                # Is a mention?
                if self._validate_node(node):
                    self._add_mention(node)
                    # Order the children of the nodes
                ordered_children = sorted(
                    self.graph_builder.get_syntactic_children(node), key=lambda child: child["ord"])
                # Add the children to the search
                nodes.extend(ordered_children)

    def _process_constituent_bfst(self, s_chunk):
        """Process each constituent of the chunk in a breath-first-transverse
        :param s_chunk: The chunk where each element must be traversed separately
        """
        # Visit each constituent in a BFT algorithm
        ordered_constituents = sorted(self.graph_builder.get_syntactic_children(s_chunk),
                                      key=lambda child: child["ord"])
        self.sentence_mentions_bft_constituent_order_current = []
        self.sentence_mentions_bft_constituent_order_lists.append(self.sentence_mentions_bft_constituent_order_current)
        for constituent in ordered_constituents:
            self._extract_mentions_from_constituent(constituent)

    def _process_named_entities(self, sentence):
        """Add the named entities to the candidates.

        For every entity in the sentence:
            + Store as a mention
            + Add their span for the no inside NE restriction
         : param sentence: The base node for the sentence named entities. usually the root node.
        """
        for entity in self.graph_builder.get_sentence_named_entities(sentence):
            entity_span = entity["span"]
            # check is not already added
            if entity_span not in self.candidates_span:
                # Allocate in the tree
                constituent = self.tree_utils.allocate_named_entities(entity, sentence)
                # Add the mention to registers
                self.candidates_span.append(entity_span)
                self.named_entities_span.append(entity_span)
                self.named_entities_by_constituent[constituent["id"]].append(entity)

    def process_sentence(self, sentence):
        """ Extract al the mentions of the Order all graph syntactic trees in filtered breath-first-transverse.

        :param sentence: The sentence whose mentions are wanted.
        """
        self.sentence_mentions_bft_order = []
        self.sentence_mentions_bft_constituent_order_lists = []
        self.sentence_mentions_bft_constituent_order_current = None
        self.named_entities_by_constituent = defaultdict([].__class__)
        # The spans are used to avoid duplicate mentions and mention inside NE
        self.candidates_span = []
        self.named_entities_span = []
        # Prepare the Named entities before the tree traversal
        self._process_named_entities(sentence)
        # Skip useless Root nodes
        syntax_root = self.tree_utils.skip_root(sentence)
        # Thought the rabbit hole
        self._process_constituent_bfst(s_chunk=syntax_root)
        # Text appearance order
        sentence_mentions_textual_order = [
            mention["id"] for mention in sorted(
                self.sentence_mentions_bft_order,
                key=lambda m: m["span"])]
        sentence_mentions_bst_order = [mention["id"] for mention in self.sentence_mentions_bft_order]
        sentence_mentions_bst_order_list = [[mention["id"] for mention in mention_list]
                                            for mention_list in self.sentence_mentions_bft_constituent_order_lists]
        return sentence_mentions_bst_order, sentence_mentions_textual_order, sentence_mentions_bst_order_list

    def _set_appositive(self, mention):
        """ Set the mention as appositive.
        @param mention: The mention that is appositive
        """
        mention["appositive"] = self.tree_utils.is_appositive_construction_child(mention)

    def _set_predicative_nominative(self, mention):
        """ Set the mention as predicative-nominative.
        @param mention: The mention that is predicative-nominative.
        """
        mention["predicative_nominative"] = self.tree_utils.is_predicative_nominative(mention)

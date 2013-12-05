# coding=utf-8
""" The kaf version of the graph builder

"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ..graph.graph_builder import BaseGraphBuilder
from ..graph.xutils import GraphWrapper
from ..resources import tree
from ..resources.dictionaries import verbs, pronouns
from ..resources.tagset import ner_tags, pos_tags, constituent_tags

from pykaf import KafDocument
from collections import defaultdict, deque
from operator import itemgetter
import logging


class KafAndTreeGraphBuilder(BaseGraphBuilder):
    """Extract the info from KAF documents and TreeBank."""
    kaf_document_property = "kaf"
    kaf_id_property = "kaf_id"
    kaf_offset_property = "offset"

    def __init__(self, logger=logging.getLogger("KafGraphBuilder")):
        super(KafAndTreeGraphBuilder, self).__init__()
        self.logger = logger
        self.syntax_count = 0
        self.leaf_count = 0
        self.kaf = None
        self.sentence_order = 0
        self.utterance = -1
        self.speakers = []
        self.terms_pool = []
        self.term_by_id = dict()
        self.term_by_word_id = dict()
        self.entities_by_word = defaultdict(set)
        self.entities = list()
        self.max_utterance = 1
        self.doc_type = "unknown"
        self._sentences = None
        self.graph_utils = None

    def set_graph(self, graph):
        """ Set the graph where this builders works
        @param graph: The graph target of this builder
        """
        super(self.__class__, self).set_graph(graph)
        self.graph_utils = SyntacticTreeUtils(graph)

    def get_graph_utils(self):
        """  Returns a object that provide complex relation finder for graph nodes.
        @return: The utility object
        """
        return self.graph_utils

    def process_document(self, graph, document):
        """ Get a document and prepare the graph an the graph builder to sentence by sentence
         processing of the document.
        @param graph: The graph where the kaf info is loaded
        @param document: A tuple that contains (the KAF,Sentences or none, speakers or none)
        """
        self.graph = graph
        # Counter to order the sentences inside a text. A easier way to work with sentences that order
        self.sentence_order = 1
        if document[1]:
            self._sentences = document[1].strip().split("\n")
        # If speaker is None store None otherwise store split speaker file
        if document[2]:
            # Remove the blank lines and split
            self.speakers = []
            current_speaker = None
            self.max_utterance = -1
            for line in document[2].split("\n"):
                if line == "":
                    continue
                self.speakers.append(line)
                if current_speaker != line:
                    self.max_utterance += 1
                    current_speaker = line

            # A doc is a conversation if exist two o more speakers in it
            if self.max_utterance > 1:
                self.doc_type = "conversation"
            else:
                self.doc_type = "article"
        else:
            self.speakers = []
            self.max_utterance = 1
            self.doc_type = "article"
        self.utterance = -1
        self.parse_kaf(kaf_string=document[0].strip())

    def get_sentences(self):
        """ Get the sentences of the document.
        @return: A list of trees(kaf nodes or Penn-treebank strings)
        """
        if self._sentences:
            return self._sentences
        else:
            return self.kaf.get_constituency_trees()

    def parse_kaf(self, kaf_string):
        """ Parse al tha kaf info tho the graph except of sentence parsing.
        @param kaf_string:
        """

        self.terms_pool = []
        # Store original kaf for further recreation
        self.kaf = KafDocument(kaf_stream=kaf_string)
        GraphWrapper.set_graph_property(self.graph, self.kaf_document_property, self.kaf)
        self.set_terms(self.kaf)
        self.set_entities(self.kaf)
        self.set_dependencies(self.kaf)

    def process_sentence(self, graph, sentence, root_index, sentence_namespace):
        """Add to the graph the morphological, syntactical and dependency info contained in the sentence.

        :param graph: The graph where the kaf info is loaded
        :param sentence: the sentence to parse
        :param sentence_namespace: prefix added to all nodes ID strings.
        :param root_index: The index of the root node
        """
        self.graph = graph
        sentence_id = sentence_namespace
        sentence_label = sentence_namespace

        # Sentence Root
        sentence_root_node = self.add_sentence(root_index=root_index, sentence_form="", sentence_label=sentence_label,
                                               sentence_id=sentence_id)
        sentence_root_node["graph"] = graph
        sentence_root_node["sentence_order"] = self.sentence_order

        first_constituent = self.parse_syntax(sentence=sentence, syntactic_root=sentence_root_node)

        # copy the properties to the root
        if first_constituent != sentence_root_node:
            sentence_root_node["lemma"] = first_constituent["lemma"]
            sentence_root_node["form"] = first_constituent["form"]
            sentence_root_node["span"] = first_constituent["span"]
            sentence_root_node["ord"] = first_constituent["ord"]
            sentence_root_node["begin"] = first_constituent["begin"]
            sentence_root_node["end"] = first_constituent["end"]

        self.sentence_order += 1
        # Statistics
        self.statistics_sentence_up()
        #self.show_graph()
        # Return the generated context graph
        return sentence_root_node

    def set_entities(self, kaf):
        """ Extract the entities of the kaf and add to the file

        @param kaf: The kaf file manager
        """
        # A dict of entities that contains a list of references. A reference is a list of terms.
        self.entities_by_word = defaultdict(set)
        self.entities = list()
        for kaf_entity in kaf.get_entities():
            entity_type = kaf_entity.attrib["type"]
            entity_id = kaf_entity.attrib["eid"]
            for reference in kaf.get_entity_references(kaf_entity):
                # Fetch terms
                entity_terms = sorted(
                    [self.term_by_id[term.attrib["id"]] for term in kaf.get_entity_reference_span(reference)],
                    key=itemgetter("ord"))
                # attach 's if exist
                next_term = self.term_by_id.get("t{0}".format(int(entity_terms[-1]["id"][1:]) + 1))
                if next_term and next_term["form"] == "'s":
                    entity_terms.append(next_term)
                    # Convert ID into terms
                # Build form
                form = self.expand_node(entity_terms)
                # Build the entity
                label = "{0} | {1}".format(form, entity_type)
                entity = self.add_named_entity(entity_type=entity_type, entity_id=entity_id, label=label)
                # Set the other attributes
                entity["begin"] = entity_terms[0]["begin"]
                entity["end"] = entity_terms[-1]["end"]
                entity["form"] = form
                entity["ord"] = entity_terms[0]["span"][0], entity_terms[-1]["span"][1]
                entity["span"] = entity["ord"]

                # Link words_ids to mention as word
                for term in entity_terms:
                    self.link_word(entity, term)
                # Index the entity by its first word
                first_word_id = entity_terms[0]["id"]
                if first_word_id in self.entities_by_word:
                    self.entities_by_word[first_word_id].append(entity)
                else:
                    self.entities_by_word[first_word_id] = [entity]

    def set_terms(self, kaf):
        """ Extract the terms of the kaf and add to the graph

        @param kaf: The kaf file manager
        """
        # Words
        kaf_words = dict([(kaf_word.attrib["wid"], kaf_word) for kaf_word in kaf.get_words()])
        # Terms
        self.term_by_id = dict()
        self.term_by_word_id = dict()
        prev_speaker = None
        inside_utterance = deque()
        inside_plain_quotes = False
        for term in kaf.get_terms():
            term_id = term.attrib["tid"]
            # Fetch the words of the term values
            term_words = sorted((kaf_words[word.attrib["id"]] for word in kaf.get_terms_words(term)),
                                key=lambda x: x.attrib[self.kaf_offset_property])
            # Build term attributes
            form = self.expand_kaf_word(term_words)
            order = int(term_words[0].attrib["wid"][1:]), int(term_words[-1].attrib["wid"][1:])
            span = order
            begin = int(term_words[0].attrib[self.kaf_offset_property])
            end = int(term_words[-1].attrib[self.kaf_offset_property]) + int(term_words[-1].attrib["length"]) - 1
            # We want pennTreeBank tagging no kaf tagging
            pos = term.attrib["morphofeat"]
            kaf_id = "{0}#{1}".format(term_id, "|".join([word.attrib["wid"] for word in term_words]))
            # Clear unicode problems
            if isinstance(form, unicode):
                form = form.encode("utf8")
            try:
                lemma = term.attrib["lemma"]
                if lemma == "-":
                    raise KeyError
            except KeyError:
                lemma = form
            if isinstance(lemma, unicode):
                lemma = lemma.encode("utf8")

            label = "\n".join((form, pos, lemma, term_id))
            #Create word node
            word_node = self.add_word(
                form=form, node_id=term_id, label=label, lemma=lemma, pos=pos, order=order,
                begin=begin, end=end)
            word_node["span"] = span
            word_node[self.kaf_id_property] = kaf_id
            word_node["prev_speaker"] = prev_speaker
            if self.speakers:
                speaker = self.speakers.pop(0)
                if prev_speaker != speaker:
                    self.utterance += 1
                    prev_speaker = speaker
            else:
                speaker = "PER{0}".format(self.utterance)
            if not speaker or speaker == "-":
                speaker = "PER{0}".format(self.utterance)

            # Manage Quotation
            # TODO improve  nested quotation
            if form == "``" or (form == '"' and not inside_plain_quotes):
                self.max_utterance += 1
                inside_utterance.append(self.max_utterance)
                if form == '"':
                    inside_plain_quotes = True
            elif form == "''" or (form == '"' and inside_plain_quotes):
                if form == '"':
                    inside_plain_quotes = False
                try:
                    inside_utterance.pop()
                except IndexError:
                    self.logger.error("Unbalanced quotes")

            if len(inside_utterance):
                word_node["utterance"] = inside_utterance[-1]
                word_node["speaker"] = "PER{0}".format(inside_utterance[-1])
                word_node["quoted"] = True
            else:
                word_node["speaker"] = speaker
                word_node["utterance"] = self.utterance
                word_node["quoted"] = False

            word_node["doc_type"] = self.doc_type
            # Store term
            # ONLY FOR STANFORD DEPENDENCIES IN KAF
            for word in term_words:
                self.term_by_word_id[word.attrib["wid"]] = word_node
            self.term_by_id[term_id] = word_node
            self.terms_pool.append(word_node)
            self.statistics_word_up()
        self.leaf_count = 0

    def set_dependencies(self, kaf):
        """ Extract the dependencies of the kaf and add to the graph

        @param kaf: The kaf file manager
        """
        for dependency in kaf.get_dependencies():
            dependency_from = dependency.attrib["from"]
            dependency_to = dependency.attrib["to"]
            dependency_type = dependency.attrib["rfunc"]
            #IFS For STANFORD DEPENDENCIES IN KAF
            if dependency_from[0] == "w":
                dependency_from = self.term_by_word_id[dependency_from]
            else:
                dependency_from = self.term_by_id[dependency_from]
            if dependency_to[0] == "w":
                dependency_to = self.term_by_word_id[dependency_to]
            else:
                dependency_to = self.term_by_id[dependency_to]
            self.link_dependency(dependency_from, dependency_to, dependency_type)

    def iterate_syntax(self, syntactic_tree, parent, syntactic_root):
        """ Walk recursively over the syntax tree and add their info to the graph.
        @param syntactic_tree: The subtree to process
        @param parent: The parent node of the subtree
        @param syntactic_root: The syntactic root node of all the tree
        @return: The element created from the top of the subtree
        """
        # Aux functions
        def syntax_leaf_process(parent_node, leaf):
            """ Process a final node of the tree
            @param parent_node: The upside node of the element
            @param leaf: The node to process
            @return: The word that correspond to the leaf.
            """
            # the tree node is a leaf
            # Get the text of the tree to obtain more attributes
            self.leaf_count += 1
            text_leaf = leaf.node
            #treebank_word = leaf[0]
            is_head = "=H" in text_leaf or "-H" in text_leaf
            # Get the word node pointed by the leaf
            try:
                word_node = self.terms_pool.pop(0)
                self.last_word = word_node
            except IndexError:
                word_node = self.last_word
            # Word is mark as head
            if is_head:
                self.set_head(parent_node, word_node)
            # Word is mark as Named Entity
            if "|" in text_leaf:
                self.set_ner(constituent=word_node, ner_type=text_leaf.split("|")[-1])
            #Link the word to the node
            self.link_syntax_terminal(parent=parent_node, terminal=word_node)
            #link the word to the sentence
            self.link_root(sentence=syntactic_root, element=word_node)
            self.link_word(sentence=syntactic_root, word=word_node)
            # Enlist entities that appears in the phrase
            for mention in self.entities_by_word.get(word_node["id"], []):
                            self.add_mention_of_named_entity(sentence=syntactic_root, mention=mention)
            return word_node

        def syntax_branch_process(parent_node, branch):
            """ Process a intermediate node of the tree
            @param parent_node: The upside node of the element
            @param branch: The node to process
            @return: The constituent created from the top of the branch
            """
            # Create a node for this element
            label = branch.node
            # constituent is mark as head
            head = "=H" in label or "-H" in label
            tag = label.replace("=H", "").replace("-H", "")
            # Constituent is mark as ner
            if "|" in label:
                ner = label.split("|")[-1]
            else:
                ner = ner_tags.no_ner

            tag = tag.split("|")[0]
            order = self.syntax_count

            new_constituent = self.add_constituent(node_id="C{0}".format(order), sentence=syntactic_root, tag=tag,
                                                   order=order, label=label)
            self.set_ner(new_constituent, ner)
            self.syntax_count += 1
            # Process the children
            children = [
                self.iterate_syntax(
                    syntactic_tree=child, parent=new_constituent, syntactic_root=syntactic_root)
                for child in branch]
            children.sort(key=itemgetter("ord"))

            # Link the child with their parent (The actual processed node)
            self.link_syntax_non_terminal(parent=parent_node, child=new_constituent)
            if head:
                self.set_head(parent_node, new_constituent)
            # Add in tree named entities to entities in graph
            if constituent_tags.ner_constituent(tag):
                self.add_mention_of_named_entity(sentence=syntactic_root, mention=new_constituent)
                new_constituent["constituent"] = new_constituent
            content_text = self.expand_node(children)
            new_constituent["tree"] = branch
            new_constituent["label"] = (" | ".join((content_text, tag)))
            new_constituent["lemma"] = content_text
            new_constituent["form"] = content_text
            new_constituent["begin"] = children[0]["begin"]
            new_constituent["end"] = children[-1]["end"]
            new_constituent["ord"] = (children[0]["span"][0], children[-1]["span"][1])
            new_constituent["span"] = new_constituent["ord"]
            return new_constituent

        # Determine if the syntactic tree Node is as branch or a leaf
        if len(syntactic_tree) > 1 or not (
                isinstance(syntactic_tree[0], str) or isinstance(syntactic_tree[0], unicode)):
            constituent_or_word = syntax_branch_process(parent_node=parent, branch=syntactic_tree)
            self.syntax_count += 1
        else:
            constituent_or_word = syntax_leaf_process(parent_node=parent, leaf=syntactic_tree)
        return constituent_or_word

    def parse_syntax_kaf(self, sentence, syntactic_root):
        """ Add the syntax info from a KAF tree node

        @param sentence: The KAF tree element
        @param syntactic_root: The sentence node
        @return: the syntax root node or the first constituent
        """
        constituents_by_id = dict()
        root = None
        for non_terminal in self.kaf.get_contituent_tree_non_terminals(sentence):
            constituent_id = non_terminal.attrib["id"]
            tag = non_terminal.attrib["label"]
            order = self.syntax_count
            self.syntax_count += 1
            constituent = self.add_constituent(
                node_id=constituent_id, sentence=syntactic_root, tag=tag, order=order, label=tag)
            constituent["ner"] = ner_tags.no_ner
            if constituent_tags.root(tag):
                root = constituent
            constituents_by_id[constituent_id] = constituent
        constituents = constituents_by_id.values()
        terminals = self.kaf.get_contituent_tree_terminals(sentence)
        terminals_words = dict([
            (terminal.attrib["id"], [self.term_by_id[target_term.attrib["id"]]
                                     for target_term in self.kaf.get_contituent_terminal_words(terminal)])
            for terminal in terminals])
        edges = self.kaf.get_contituent_tree_edges(sentence)
        edges.reverse()
        for edge in edges:
            # The edges have a down-top direction
            target_id = edge.attrib["to"]
            source_id = edge.attrib["from"]
            target = constituents_by_id[target_id]
            # select link type in base of the source node type
            if source_id.startswith("n"):
                source = constituents_by_id[source_id]
                self.link_syntax_non_terminal(parent=target, child=source)
                # Set the head of the constituent
                if edge.attrib.get("head", False):
                    self.set_head(target, source)
            else:
                source = terminals_words[source_id]
                if len(source) == 1 and target["tag"] == source[0]["pos"]:
                    word = source[0]
                    self.link_root(sentence=syntactic_root, element=word)
                    nexus_constituent = constituents_by_id[target_id]
                    constituents_by_id[target_id] = word
                    self.remove(nexus_constituent)
                    constituents.remove(nexus_constituent)
                    self.link_word(sentence=syntactic_root, word=word)
                    # Enlist entities that appears in the phrase

                    for mention in self.entities_by_word.get(word["id"], []):
                        self.add_mention_of_named_entity(sentence=syntactic_root, mention=mention)
                else:
                    for word in source:
                        self.link_root(sentence=syntactic_root, element=word)
                        self.link_syntax_terminal(parent=target, terminal=word)
                        self.link_word(sentence=syntactic_root, word=word)
                        # Enlist entities that appears in the phrase
                        for mention in self.entities_by_word.get(word["id"], []):
                            self.add_mention_of_named_entity(sentence=syntactic_root, mention=mention)
                        # Set the head of the constituent
                    self.set_head(target, source[-1])

        # Build constituent child based values
        for constituent in constituents:
            children = self.get_words(constituent)
            children.sort(key=itemgetter("ord"))
            content_text = self.expand_node(children)
            constituent["label"] = (" | ".join((content_text, constituent["tag"])))
            constituent["lemma"] = self.expand_node_lemma(children)
            constituent["form"] = content_text
            constituent["begin"] = children[0]["begin"]
            constituent["end"] = children[-1]["end"]
            constituent["ord"] = (children[0]["span"][0], children[-1]["span"][1])
            constituent["span"] = constituent["ord"]

        # link the tree with the root
        if root:
            self.link_syntax_non_terminal(parent=syntactic_root, child=root)
        else:
            self.logger.warning(
                "No ROOT found, used the first constituent, sentence:".format(syntactic_root["sentence_order"]))
            self.link_syntax_non_terminal(parent=syntactic_root, child=constituents[0])
        # Set the head of the constituent
        self.set_head(syntactic_root, root)
        return root

    def parse_syntax(self, sentence, syntactic_root):
        """ Parse the syntax of the sentence.

        @param sentence:  The sentence
        @param syntactic_root:
        @return: The upper node of the syntax tree.
        """
        # Convert the syntactic tree
        if type(sentence) is str:
            # Is a plain Penn-tree
            sentence = self.clean_penn_tree(sentence)
            syntactic_tree = tree.Tree(sentence)
            # Call to the recursive function
            return self.iterate_syntax(
                syntactic_tree=syntactic_tree, parent=syntactic_root, syntactic_root=syntactic_root)
        else:
            # Is a kaf tree
            return self.parse_syntax_kaf(sentence=sentence, syntactic_root=syntactic_root)

    # AUX FUNCTIONS
    @staticmethod
    def expand_kaf_word(words):
        """ Rebuild the text form from a list of kaf words
        @param words: a list of KAF words
        @return: the form of all words separated by comas.
        """
        text = " ".join([word.text for word in words])
        return text.strip()

    @staticmethod
    def expand_node(terms):
        """ Rebuild the from of a element
        @param terms: The ordered term lsit of this element
        @return: The form of the element
        """
        text = " ".join([term["form"] for term in terms])
        return text.strip()

    @staticmethod
    def expand_node_lemma(terms):
        """ Rebuild the lemma of a element
        @param terms: The ordered term list of this element
        @return: The form of the element
        """
        text = " ".join([term["lemma"] for term in terms])
        return text.strip()

    @staticmethod
    def clean_penn_tree(penn_tree):
        """ Clean from the tree all knows problems
        @param penn_tree: the plain tree
        @return: cleaned tree
        """
        penn_tree = penn_tree.strip()
        return penn_tree


class SyntacticTreeUtils():
    def __init__(self, graph):
        self.graph = graph
        self.graph_builder = GraphWrapper.get_graph_property(self.graph, 'graph_builder')
        self.graph.graph["utils"] = self

    def skip_root(self, sentence_root):
        """Get the first chunk of the sentence (usually S) Skip al ROOT nodes,created by the parser o the graph builder.
        Skip all the dummy roots crated by the parsers/graph builder.
        :param sentence_root: The syntactic tree root node.
        """
        chunk = sentence_root
        while chunk and (chunk["tag"] == self.graph_builder.root_pos):
            chunk = self.graph_builder.get_syntactic_children(chunk)[0]
            #TODO Warning if more than one child
        return chunk

# Allocation of Named Entities
    def get_span_constituent(self, sentence, span):
        """ Try to fit a span (a group of sequential words) into a existing constituent.

        :param sentence: The sentence where the word must be allocated.
        :param span: The list of word that must be allocated.
        """
        nodes = self.graph_builder.get_syntactic_children(sentence)
        while nodes:
            node = nodes.pop()
            node_span = node["span"]
            if node_span == span:
                return node
            children = self.graph_builder.get_syntactic_children(node)
            if not (node_span[0] > span[0] or node_span[-1] < span[-1]):
                nodes.extend(children)
        return None

    def get_plausible_head_word(self, words):
        """ Get a Head word for the NE that preserves the head coherence.

        Find the words of the NE that are heads. If more than one are head use the head assign rules( NP cases) with
        the head word to select the head. If no head is contained in the bag of word use every word instead of head
        words.

        #  head word assignment preferences for NP cases:
        # "NN", "NNP", "NNPS", "NNS", "NX", "JJR", "POS"
        """

        head_words = [word for word in words if self.graph_builder.is_head(word)]
        for pos in pos_tags.head_rules:
            for word in head_words:
                if word["pos"] == pos:
                    return word

        for pos in pos_tags.head_rules:
            for word in words:
                if word["pos"] == pos:
                    return word
        return words[0]

    def get_plausible_constituent(self, head):
        """ Get the highest NP that has the same head.

        Get the constituent that complains these restriction:
            + Have the same terminal head.
            + Is NP.
            + Is the highest NP of the first chain of NPs.

        If no valid NP is found use the constituent of the head.

        # Source StanfordCoreNLP::MentionExtractor.Java::Class:MentionExtractor:Arrage
        :param head: the terminal head that must be the head of the constituent.
        """

        base_constituent = head
        constituent = self.graph_builder.get_syntactic_parent(head)
        valid_constituent = None
        # Climb until head chain is broken
        while constituent and self.graph_builder.is_head(constituent) and \
                self.graph_builder.get_head(constituent)["id"] == head["id"]:
            # If is a valid constituent store it
            if constituent_tags.noun_phrases("tag" in constituent and constituent["tag"]):
                valid_constituent = constituent
            # If already have a valid constituent and valid constituent chain is broken, Stop the search
            elif valid_constituent:
                break
                # Climb
            constituent = self.graph_builder.get_syntactic_parent(constituent)
            # Fallback constituent
        if not valid_constituent:
            valid_constituent = base_constituent
        return valid_constituent

    def allocate_named_entities(self, entity, sentence):
        """ Try to set a terminal head and a constituent of a named entity.

         The constituent and the head is used to order the mention in the sieve searching.
        :param sentence: The sentence where the word must be allocated.
        :param entity: The named entity that must be allocated.
        """
        # Find a plausible terminal head
        entity_span = entity["span"]
        # Try to find a constituent that fit the mention span
        valid_constituent = self.get_span_constituent(sentence, entity_span)
        if valid_constituent:
            head = self.graph_builder.get_head(valid_constituent)
        else:
            # Use the head finder
            head = self.get_plausible_head_word(self.graph_builder.get_words(entity))
        if not head:
            #TODO Change into warning
            raise Exception("Unable to fit NE")
            #TODO check if this is useful with a previous constituent
        # With the artificial Terminal head find a plausible NP constituent
        constituent = self.get_plausible_constituent(head)
        self.graph_builder.set_head(entity, head)
        # Used in speaker sieve, The head word is the relevant info source
        entity["constituent"] = constituent
        self.graph_builder.link_root(entity, self.graph_builder.get_root(constituent))
        #entity["root"] = constituent["root"]
        return constituent

# Syntax complex relations
    def is_role_appositive(self, candidate, mention):
        """ Return if the candidate is the role appositive of the mention.
        """
        if not self.graph_builder.same_sentence(mention, candidate):
            return False
        # If candidate or mention are NE use their constituent
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if mention["type"] == "named_entity":
            mention = mention["constituent"]

        # The Candidate is headed by a noun.
        candidate_head = self.graph_builder.get_head_word(candidate)
        if not candidate_head or not pos_tags.all_nouns(candidate_head["pos"]):
            return False
            # The Candidate appears as a modifier of a NP
        candidate_syntactic_father = self.graph_builder.get_syntactic_parent(candidate)
        if not constituent_tags.noun_phrases(candidate_syntactic_father["tag"]):
            return False
            # The NP whose head is the mention
        return mention["id"] == self.graph_builder.get_head(candidate_syntactic_father)["id"]

    def is_appositive_construction_child(self, constituent):
        """ Check if the mention is in a appositive construction.

        "NP=m1 < (NP=m2 $.. (/,/ $.. NP=m3))";
        "NP=m1 < (NP=m2 $.. (/,/ $.. (SBAR < (WHNP < WP|WDT=m3))))";
        "/^NP(?:-TMP|-ADV)?$/=m1 < (NP=m2 $- /^,$/ $-- NP=m3 !$ CC|CONJP)";
        "/^NP(?:-TMP|-ADV)?$/=m1 < (PRN=m2 < (NP < /^NNS?|CD$/ $-- /^-LRB-$/ $+ /^-RRB-$/))";

        @param constituent: The mention to check
        """
        if "contituent" in constituent:
            constituent = constituent["constituent"]

        # TODO Improve the precision
        parent = self.graph_builder.get_syntactic_parent(constituent)
        if not constituent_tags.noun_phrases(parent["tag"]):
            return False
        siblings = self.graph_builder.get_syntactic_sibling(constituent)
        for sibling in siblings:
            if "pos" in sibling and pos_tags.conjunction(sibling["pos"]):
                return False
        if len(siblings) >= 3:
            first_child = siblings[0]
            second_child = siblings[1]
            if ("tag" in first_child) and constituent_tags.noun_phrases(first_child["tag"]) and\
                    second_child["form"] == ",":
                if len(siblings) == 3:
                    return True
                elif len(siblings) > 3:
                    return siblings[3]["form"] == ","
        else:
            return False

    def is_predicative_nominative(self, constituent):
        """ Check if the constituent is a predicate in a predicative nominative mention

        Stanford check for the relation:
        # "S < (NP=m1 $.. (VP < ((/VB/ < /^(am|are|is|was|were|'m|'re|'s|be)$/) $.. NP=m2)))";
        # "S < (NP=m1 $.. (VP < (VP < ((/VB/ < /^(be|been|being)$/) $.. NP=m2))))";

        @param constituent: The mention to check
        """
        # The constituent is in a VP that start with a copulative verb
        parent = self.graph_builder.get_syntactic_parent(constituent)
        if constituent_tags.verb_phrases(parent["tag"]):
            for child in self.graph_builder.get_syntactic_children(parent):
                if child["span"] < constituent["span"] \
                        and "pos" in child \
                        and pos_tags.verbs(child["pos"]) \
                        and child["form"] in verbs.copulative:
                    return True
        return False

    def is_bare_plural(self, constituent):
        """ Check if the constituent is Bare plural.
        @param constituent: The constituent to check
        @return: Boolean
        """
        span = constituent["span"]
        return (span[0] - span[1] == 0) and pos_tags.bare_plurals(self.graph_builder.get_constituent_words(constituent)[0]["pos"])

    def is_relative_pronoun(self, first_constituent, second_constituent):
        """ Check if tho constituents are in relative pronoun construction. Also mark they.
        @param first_constituent:
        @param second_constituent:
        @return: Boolean
        """

        #NP < (NP=m1 $.. (SBAR < (WHNP < WP|WDT=m2)))
        if not self.graph_builder.same_sentence(first_constituent, second_constituent):
            return False
        if second_constituent["form"].lower() not in pronouns.relative:
            return False
        enclosing_np = self.graph_builder.get_syntactic_parent(first_constituent)

        upper = self.graph_builder.get_syntactic_parent(second_constituent)
        while upper and (upper["type"] != self.graph_builder.root_type):
            if self.graph_builder.is_inside(upper["span"], enclosing_np["span"]):
                upper = self.graph_builder.get_syntactic_parent(upper)
            elif upper["id"] == enclosing_np["id"]:
                #TODO check path element
                #TODO m1 and m2 order
                return True
            else:
                return False

        return False
        # return set(filter(lambda X: X["tag"] in
        #                             constituent_tags.subordinated, mention.in_neighbours())).intersection(
        #     set(filter(lambda X: X["tag"] in
        #                          constituent_tags.subordinated, candidate.out_neighbours())))

    def check_sibling_property(self, base_index, siblings, _property, check_function):
        constituent = None
        index = 0
        for index, sibling in enumerate(siblings[base_index:]):
            if _property in sibling and  check_function(sibling[_property]):
                constituent = sibling
                break
        return constituent, index

    def pleonastic_it(self, mention):
        #TODO improve the multi language
        """ Determine if the mention is pleonastic.
        @param mention: THe mention to check
            "@NP < (PRP=m1 < it|IT|It) $.. (@VP < (/^V.*/ < /^(?i:is|was|be|becomes|become|became)$/ $.. (@VP < (VBN $.. @S|SBAR))))"
            // in practice, go with this one (best results)

            "NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (ADJP $.. (/S|SBAR/))))"
            "NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (ADJP < (/S|SBAR/))))"

            "NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (NP < /S|SBAR/)))"
            "NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (NP $.. ADVP $.. /S|SBAR/)))"

            "NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (VP < (VBN $.. /S|SBAR/))))))"

            "NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (ADJP $.. (/S|SBAR/))))))" // extraposed. OK 1/2 correct; need non-adverbial case
            "NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (ADJP < (/S|SBAR/))))))" // OK: 3/3 good matches on dev; but 3/4 wrong on WSJ

            "NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (NP < /S|SBAR/)))))"
            "NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (NP $.. ADVP $.. /S|SBAR/)))))"

            "NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:seems|appears|means|follows)/) $.. /S|SBAR/))"

            "NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:turns|turned)/) $.. PRT $.. /S|SBAR/))"
        """
        # NP < (PRP=m1) $..
        # Is a "it" pronoun
        if mention["form"].lower() in pronouns.pleonastic:
            return False
        constituent = ('constituent'in mention and mention['constituent']) or mention
        father = self.graph_builder.get_syntactic_parent(constituent)
        # Is a child of a NP
        if not constituent_tags.noun_phrases(father["form"]):
            return False

        # Have a (next) sibling that is a VP
        wrapper_NP_siblings = self.graph_builder.get_syntactic_children(father)
        wrapper_NP_index = wrapper_NP_siblings.index(father)

        #(VP <
        verb_phrase, verb_phrase_index = self.check_sibling_property(
            wrapper_NP_index, wrapper_NP_siblings, "tag", constituent_tags.verb_phrases)

        if not verb_phrase:
            return False

        #((/^V.*/ < /^(?:is|was|become|became)/)
        VP_constituents = self.graph_builder.get_syntactic_children(verb_phrase)
        valid_verb, valid_verb_index = self.check_sibling_property(
            0, VP_constituents, "form", lambda x: x in verbs.pleonastic_verbs)

        if not valid_verb:
            #((/^V.*/ < /^(?:seems|appears|means|follows)/)
            alternative_a_valid_verb, alternative_a_valid_verb_index = self.check_sibling_property(
                0, VP_constituents, "form", lambda x: x in verbs.alternative_a_pleonastic_verbs)
            if alternative_a_valid_verb:
                #  $.. /S|SBAR/)
                sbar, sbar_index = self.check_sibling_property(
                    VP_constituents, alternative_a_valid_verb_index, "tag", constituent_tags.simple_or_sub_phrase)
                return sbar
            alternative_b_valid_verb, alternative_b_valid_verb_index = self.check_sibling_property(
                0, VP_constituents, "form", lambda x: x in verbs.alternative_b_pleonastic_verbs)
            if alternative_b_valid_verb:
                # $.. PRT $.. /S|SBAR/))
                particle, particle_index = self.check_sibling_property(
                    VP_constituents, alternative_b_valid_verb_index, "tag", constituent_tags.particle_constituents)
                sbar, sbar_index = self.check_sibling_property(
                    VP_constituents, particle_index, "tag", constituent_tags.simple_or_sub_phrase)
                return sbar

        #(MD $.. (VP < ((/^V.*/ < /^(?:be|become)/)
        if not valid_verb:
            auxiliar_verb, auxiliar_verb_index = self.check_sibling_property(
                0, VP_constituents, "pos", pos_tags.modals)
            if auxiliar_verb:
                verb_phrase, verb_phrase_index = self.check_sibling_property(
                    wrapper_NP_index, wrapper_NP_siblings, "tag", constituent_tags.verb_phrases)
                VP_constituents = self.graph_builder.get_syntactic_children(verb_phrase)
                valid_verb, valid_verb_index = self.check_sibling_property(
                    0, VP_constituents, "form", lambda x: x in verbs.pleonastic_verbs)

        if not valid_verb:
            return False

        constituents_pri, constituents_pri_index = ([], 0)
        constituents_sec, constituents_sec_index = ([], 0)

        #$.. (@VP < (VBN $.. @S|SBAR))))
        second_verb, second_verb_index = self.check_sibling_property(
            valid_verb_index, VP_constituents, "tag", constituent_tags.verb_phrases)
        if second_verb:
            children = self.graph_builder.get_syntactic_children(second_verb)
            verb_form = self.check_sibling_property(
                0, children, "pos", constituent_tags.past_participle_verb)
            if verb_form:
                constituents_pri, constituents_pri_index = self.check_sibling_property(
                    0, children, "pos", constituent_tags.past_participle_verb)

        # $.. (ADJP $.. (/S|SBAR/))))
        # $.. (ADJP < (/S|SBAR/))))
        adjectival_phrase, adjectival_phrase_index = self.check_sibling_property(
            valid_verb_index, VP_constituents, "tag", constituent_tags.adjectival_prhases)
        if second_verb:
            children = self.graph_builder.get_syntactic_children(adjectival_phrase)
            constituents_pri, constituents_pri_index = (VP_constituents, adjectival_phrase_index)
            constituents_sec, constituents_sec_index = (children, 0)

        # $.. (NP < /S|SBAR/)))
        # $.. (NP $.. ADVP $.. /S|SBAR/)))
        noun_phrase, noun_phrase_index = self.check_sibling_property(
            valid_verb_index, VP_constituents, "tag", constituent_tags.noun_phrases)
        if second_verb:
            children = self.graph_builder.get_syntactic_children(noun_phrase)
            constituents_pri, constituents_pri_index = (0, children)
            adverbial_phrase, adverbial_phrase_index = self.check_sibling_property(
                noun_phrase_index, VP_constituents, "tag", constituent_tags.noun_phrases)
            if adjectival_phrase:
                constituents_sec, constituents_sec_index = (VP_constituents, adverbial_phrase_index)

        sbar1, sbar1_index = self.check_sibling_property(
            constituents_pri_index, constituents_pri, "tag", constituent_tags.simple_or_sub_phrase)
        sbar2, sbar1_index = self.check_sibling_property(
            constituents_sec_index, constituents_sec, "tag", constituent_tags.simple_or_sub_phrase)

        return sbar1 or sbar2
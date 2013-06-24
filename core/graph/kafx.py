import logging
from collections import defaultdict
from graph.xutils import GraphWrapper
from resources import tree
from pykaf.kaf import KafDocument
from graph.graph_builder import BaseGraphBuilder
from resources.dictionaries import verbs
from resources.tagset import ner_tags, pos_tags, constituent_tags

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '3/13/13'


class KafAndTreeGraphBuilder(BaseGraphBuilder):
    """Extract the info from KAF documents and TreeBank."""
    kaf_document_property = "kaf"
    kaf_id_property = "kaf_id"

    def __init__(self, logger=logging.getLogger("KafGraphBuilder")):
        self.logger = logger
        self.graph_properties[self.kaf_document_property] = "object"
        self.vertex_properties[self.kaf_id_property] = "string"
        self.syntax_count = 0

    def preprocess_sentences(self, graph, document):
        self.graph = graph
        self.span = 1
        sentences = document[1].split("\n")
        self.parse_kaf(kaf_string=document[0])
        return sentences

    def process_sentence(self, graph, sentence, root_index, sentence_namespace):
        """Add to the graph the morphological, syntactical and dependency info contained in the sentence.

        sentence: the sentence to parse
        sentenceNamespace:: prefix added to all nodes ID strings.
        separator: character or string used for create the nodes ID string.
        """
        self.graph = graph
        base_span = self.span
        sentence_id = sentence_namespace
        sentence_label = sentence_namespace

        # Sentence Root
        sentence_root_node = self.add_sentence(root_index=root_index, sentence_form="", sentence_label=sentence_label,
                                               sentence_id=sentence_id)
        sentence_text = self.parse_syntax(sentence=sentence, syntactic_root=sentence_root_node,
                                          sentenceNamespace=sentence_namespace)
        # Return the generated context graph
        sentence_root_node["lemma"] = sentence_text
        sentence_root_node["form"] = sentence_text
        sentence_root_node["span"] = (base_span, self.span)
        self.statistics_sentence_up()
        return sentence_root_node

    def parse_kaf(self, kaf_string):

        self.word_pool = []
        # Store original kaf for further recreation
        kaf = KafDocument(kaf_stream=kaf_string)
        GraphWrapper.set_graph_property(self.graph, self.kaf_document_property, kaf)
        # Words
        kaf_words = dict([(kaf_word.attrib["wid"], kaf_word.text) for kaf_word in kaf.get_words()])
        # Terms
        term_by_id = dict()
        for term in kaf.get_terms():
            # Fetch the words values
            term_id = term.attrib["tid"]
            words = kaf.get_terms_words(term)
            form = " ".join([kaf_words[word.attrib["id"]] for word in words])
            if isinstance(form, unicode):
                form = form.encode("utf8")
            kaf_id = "{0}#{1}".format(term_id, "|".join([word.attrib["id"] for word in words]))
            try:
                lemma = term.attrib["lemma"]
            except KeyError:
                lemma = form
                # We want pennTreeBank tagging no kaf tagging
            pos = term.attrib["morphofeat"]
            if isinstance(lemma, unicode):
                lemma = lemma.encode("utf8")
            order = int(term_id[1:])
            label = "\n".join((form, pos, lemma, term_id))
            #Create word node
            word_node = self.add_word(
                form=form, wid=term_id, label=label, lemma=lemma, ner=ner_tags.no_ner, pos=pos, head=False, order=order)
            word_node[self.kaf_id_property] = kaf_id
            # Store the words
            term_by_id[term_id] = word_node
            self.word_pool.append(word_node)
            self.statistics_word_up()

        #A dict of entities that contains a list of references. A reference is a list of terms.
        self.entities_by_word = defaultdict(set)
        self.entities = list()
        # Entities
        for kaf_entity in kaf.get_entities():
            entity_type = kaf_entity.attrib["type"]
            entity_id = kaf_entity.attrib["eid"]
            for reference in kaf.get_entity_references(kaf_entity):
                # Create
                words = sorted((term.attrib["id"] for term in kaf.get_entity_reference_span(reference)))
                # attach 's if exist
                next_term_id = "t{0}".format(int(words[-1][1:]) + 1)
                if term_by_id[next_term_id]["form"] == "'s":
                    words.append(next_term_id)
                    #
                label = " ".join((term_by_id[word]["form"]) for word in words)
                entity = self.add_named_entity(entity_type=entity_type, entity_id=entity_id, label=label)
                # Link words to mention as terminals
                for term_id in words:
                    self.syntactic_terminal_link(entity, term_by_id[term_id])
                    # Set the other attributes
                entity["form"] = label
                entity["ord"] = int(words[0][1:])
                entity["span"] = (int(words[0][1:]), int(words[-1][1:]))
                self.entities_by_word[words[-1]] = entity

    def parse_syntax(self, sentence, syntactic_root, sentenceNamespace):

        # Convert the syntactic tree
        syntactic_tree = tree.Tree(sentence)
        self.word_count += 1

        entities = []

        def Iterate_Syntax(syntactic_tree, parent_node):
            """Walk recursively over the syntax tree and add their info to the graph."""
            # Aux functions

            def syntax_leaf_process(parent_node, leaf):
                # the tree node is a leaf
                # Get the word node pointed by the leaf
                word_node = self.word_pool.pop(0)
                word_node["span"] = (self.span, self.span)
                self.span += 1
                # Get the text of the tree to obtain more attributes
                text_leaf = leaf.node
                treebank_word = leaf[0]
                head = "=H" in text_leaf or "-H" in text_leaf
                # Word is mark as head
                if head:
                    self.set_head(parent_node, word_node)

                # Word is mark as Named Entity
                if "|" in text_leaf:
                    word_node["ner"] = text_leaf.split("|")[-1]
                    #Link the word to the node
                self.syntactic_terminal_link(parent_node=parent_node, terminal_node=word_node)
                #link the word to the sentence
                self.link_word(sentence_root_node=syntactic_root, word_node=word_node)
                # Generate the text
                content_text = treebank_word
                # Enlist entities that appears in the phrase
                if word_node["id"] in self.entities_by_word:
                    self.add_named_mention(root=syntactic_root, mention=self.entities_by_word[word_node["id"]])
                return content_text

            def syntax_branch_process(parent_node, branch):
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

                new_node = self.add_constituent(node_id="C{0}".format(self.syntax_count), form="", head=head,
                                                root=syntactic_root, label=label, lemma="", ner=ner, tag=tag,
                                                order=order)
                self.syntax_count += 1
                # Link the child with their parent (The actual processed node)
                self.syntax_tree_link(parent=parent_node, child=new_node)
                if head:
                    self.set_head(parent_node, new_node)
                first_span = self.span
                # Process the children
                content_text = []

                for child in branch:
                    # Fetch the text contained
                    content_text_part = Iterate_Syntax(syntactic_tree=child, parent_node=new_node)
                    # Append the text
                    content_text.append(content_text_part)
                    # Rebuild the attributes composed from children info
                content_text = " ".join(content_text)

                # Set the rebuild attributes
                new_node["label"] = ("\n".join((content_text, tag)))
                new_node["lemma"] = content_text
                new_node["form"] = content_text
                new_node["span"] = (first_span, self.span - 1)
                return content_text

            # Determine if the syntactic tree Node is as branch or a leaf
            if len(syntactic_tree) > 1 or not (
                    isinstance(syntactic_tree[0], str) or isinstance(syntactic_tree[0], unicode)):
                content_text = syntax_branch_process(parent_node=parent_node, branch=syntactic_tree)
                self.syntax_count += 1
            else:
                content_text = syntax_leaf_process(parent_node=parent_node, leaf=syntactic_tree)
            return content_text

            # Call to the recursive function

        return Iterate_Syntax(syntactic_tree=syntactic_tree, parent_node=syntactic_root)


class SyntacticTreeUtils():
    def __init__(self, graph):
        self.graph = graph
        self.graph_builder = GraphWrapper.get_graph_property(self.graph, 'graph_builder')
        self.graph.graph["utils"] = self

    # Sentence Related

    def same_sentence(self, nodeA, nodeB):
        """ Check if the nodes are in the same sentence
        """
        return nodeA["root"] == nodeB["root"]

    def sentence_distance(self, nodeA, nodeB):
        """ Get the distance between the sentences of 2 nodes( 0 for same sentence nodes).

        The distance is always a positive number.
        """
        root_a = nodeA["root"]
        root_b = nodeB["root"]
        return abs(root_a["ord"] - root_b["ord"])

    def get_sentence_words(self, root):
        """Get the (Sorted)words contained in a sentence.

         This method not traverse the syntactic tree, used the root direct links. NOT USE WITH CONSTITUENT.
        :param root: the root node  of the sentence
        """
        return sorted(GraphWrapper.get_filtered_by_type_out_neighbours(
            graph=self.graph, node=root, relation_type=self.graph_builder.word_edge_type),
                      key=lambda y: y["ord"])

    def get_sentence_named_entities(self, root):
        """Get the (Sorted)named entities contained in a sentence.

         This method not traverse the syntactic tree, used the root direct links. NOT USE WITH CONSTITUENT.
        :param root: the root of the sentence
        """
        return sorted(GraphWrapper.get_filtered_by_type_out_neighbours(
            graph=self.graph, node=root, relation_type=self.graph_builder.named_entity_edge_type),
                      key=lambda y: y["ord"])

    def _skip_root(self, sentence_root):
        """Get the first chunk of the sentence (usually S) Skip al ROOT nodes,created by the parser o the graph builder.
        Skip all the dummy roots crated by the parsers/graph builder.
        :param sentence_root: The syntactic tree root node.
        """
        #    return next(next(sentence_root.out_neighbours()).out_neighbours())
        chunk = sentence_root
        while chunk and (chunk["tag"] == self.graph_builder.root_pos):
            chunk = self.get_constituent_children(chunk)[0]
            #TODO Warning if more than one child
        return chunk

    def inside(self, m1_span, m2_span):
        """Is m1 inside m2?"""
        return (m1_span[0] >= m2_span[0]) and (m1_span[1] <= m2_span[1])

    # Syntactical navigation
    def get_syntactic_sibling(self, syntactic_node):
        """ Get the sibling  sons of the same parent of a syntactic node.
        """
        syntactic_father = self.get_syntactic_parent(syntactic_node)
        siblings = self.get_constituent_children(syntactic_father)
        siblings.sort(key=lambda x: x["span"])
        return siblings

    def get_syntactic_parent(self, syntactic_node, named_entity=False):
        """Return the syntactic parent of the node(constituent or word).
        :param syntactic_node: The node chunk or word whose parent is wanted.
        """
        parents = GraphWrapper.get_filtered_by_type_in_neighbours(
            self.graph, node=syntactic_node, relation_type=self.graph_builder.syntactic_edge_type)
        for parent in parents:
            if named_entity or parent["type"] != self.graph_builder.named_entity_node_type:
                return parent
        return None

    def get_constituent_children(self, constituent):
        """Get all the syntactical children of a constituent.
        """
        return GraphWrapper.get_filtered_by_type_out_neighbours(
            graph=self.graph, node=constituent, relation_type=self.graph_builder.syntactic_edge_type)

    def get_constituent_constituents(self, constituent):
        """Get the children of the constituent that are constituents.
        """
        return [constituent for constituent in GraphWrapper.get_filtered_by_type_out_neighbours(
            graph=self.graph, node=constituent, relation_type=self.graph_builder.syntactic_edge_type)
                if constituent["type"] == self.graph_builder.syntactic_node_type]

    def get_constituent_head(self, constituent):
        """Get the head of the constituent. If a word id passed by error the word itself is returned.
        """
        graph = self.graph

        if constituent["type"] == "word":
            return constituent

        children = GraphWrapper.get_filtered_by_type_out_neighbours(
            node=constituent, relation_type=self.graph_builder.syntactic_edge_type, graph=graph)
        if len(children) == 1:
            return children[0]
        for child in children:
            if child["head"]:
                return child
        return children[0]

    def get_constituent_head_word(self, constituent):
        """ Get the terminal head (the word of the end of head chains) of the constituent.

        :param constituent: the constituent where head word is returned
        """

        def __iterate__(syntax_chunk):
            """Iteration for deep constituent """
            child = self.get_constituent_head(constituent=syntax_chunk)
            if child:
                if child["type"] == self.graph_builder.word_node_type:
                    return child
                else:
                    return __iterate__(child)
            return None

        if constituent["type"] == self.graph_builder.word_node_type:
            return constituent
        return __iterate__(constituent)

    def get_constituent_words(self, constituent):
        """ Get the words(sorted in textual order) of the constituent.

        If constituent is a word, returns the words in a list.

        :param constituent: The constituent that contains the words.
        """

        def __iterate__(syntax_chunk):
            for child in GraphWrapper.get_filtered_by_type_out_neighbours(
                    self.graph, syntax_chunk, self.graph_builder.syntactic_edge_type):
                if child["type"] == self.graph_builder.word_node_type:
                    words.append(child)
                else:
                    __iterate__(child)

                    # End of iteration

        if constituent["type"] == self.graph_builder.word_node_type:
            words = [constituent]
        else:
            words = []
            __iterate__(constituent)
        return sorted(words, key=lambda y: y["ord"])

    # Allocation of Named Entities

    def get_span_constituent(self, sentence, span):
        """ Try to fit a span (a group of sequential words) into a existing constituent.

        :param sentence: The sentence where the word must be allocated.
        :param span: The list of word that must be allocated.
        """
        nodes = self.get_constituent_children(sentence)
        while nodes:
            node = nodes.pop()
            node_span = node["span"]
            if node_span == span:
                return node
            children = self.get_constituent_children(node)
            if not (node_span[0] > span[0] or node_span[-1] < span[-1]):
                nodes.extend(children)
        return None

    def get_plausible_head_word(self, words):
        """ Get a Head word for the NE that preserves the head coherence.

        Find the words of the NE that are heads. If more than one are head use the head assign rules( NP cases) with
        the head word to select the head. If no head is conatined in the bag of word use every word instead of head
        words.

        #  head word assignament preferences for NP cases:
        # "NN", "NNP", "NNPS", "NNS", "NX", "JJR", "POS"
        """

        head_words = [word for word in words if word["head"]]
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
        base_constituent = self.get_syntactic_parent(head)
        constituent = base_constituent
        valid_constituent = None
        # Climb until head chain is broken
        while constituent and constituent["head"] and \
                        self.get_constituent_head_word(constituent) == head:
            # If is a valid constituent store it
            if constituent_tags.noun_phrases(constituent["tag"]):
                valid_constituent = constituent
            # If already have a valid constituent and valid constituent chain is broken, Stop the search
            elif valid_constituent:
                break
                # Climb
            constituent = self.get_syntactic_parent(constituent)
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
            head = self.get_constituent_head(valid_constituent)
        else:
            # Use the head finder
            head = self.get_plausible_head_word(self.get_constituent_words(entity))
        if not head:
            #TODO Change into warning
            raise Exception("Unable to fit NE")

        # With the artificial Terminal head find a plausible NP constituent
        constituent = self.get_plausible_constituent(head)
        self.graph_builder.set_head(entity, head)
        entity["head_word"] = head
        entity["constituent"] = constituent
        entity["root"] = constituent["root"]
        return constituent

    # Syntax complex relations

    def is_role_appositive(self, candidate, mention):
        """ Return if the candidate is the role appositive of the mention.
        """
        # If candidate or mention are NE use their constituent
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if mention["type"] == "named_entity":
            mention = mention["constituent"]

        # The Candidate is headed by a noun.
        candidate_head = self.get_constituent_head_word(candidate)
        if not candidate_head or not pos_tags.all_nouns(candidate_head["pos"]):
            return False
            # The Candidate appears as a modifier of a NP
        candidate_syntactic_father = self.get_syntactic_parent(candidate)
        if not constituent_tags.noun_phrases(candidate_syntactic_father["tag"]):
            return False
            # The NP whose head is the mention
        return mention == self.get_constituent_head(candidate_syntactic_father)

    def is_appositive_construction(self, mention):
        """ One mention is appositive if is the 3 child of a NP that not contains conjunctions and expansion start with
        NP , NP
        """
        parent = self.get_syntactic_parent(mention)
        if not constituent_tags.noun_phrases(parent):
            return False
        siblings = self.get_syntactic_sibling(mention)
        for sibling in siblings:
            if pos_tags.conjunctions(sibling["tag"]):
                return False
        if len(siblings) == 3:
            return constituent_tags.mention_constituents(self[siblings[0]["tag"]]) and siblings[1]["tag"] == ","
        elif len(siblings) > 3:
            return constituent_tags.mention_constituents(siblings[0]["tag"]) and \
                   siblings[1]["form"] == "," and siblings[3]["form"] == ","
        else:
            return False

    def is_predicative_nominative(self, constituent):
        """ Check if the constituent is a predicate in a predicative nominative mention

        Stanford check for the relation:
        # "S < (NP=m1 $.. (VP < ((/VB/ < /^(am|are|is|was|were|'m|'re|'s|be)$/) $.. NP=m2)))";
        # "S < (NP=m1 $.. (VP < (VP < ((/VB/ < /^(be|been|being)$/) $.. NP=m2))))";
        """
        # The constituent is in a VP that start with a copulative verb
        parent = self.get_syntactic_parent(constituent)
        if constituent_tags.verb_phrases(parent["tag"]):
            for child in self.get_constituent_children(parent):
                if child["span"] < constituent["span"] \
                        and "pos" in child \
                        and pos_tags.verbs(child["pos"]) \
                        and child["form"] in verbs.copulative:
                    return True
        return False

    def is_bare_plural(self, mention):
        span = mention["span"]
        return (span[0] - span[1] == 0) and pos_tags.bare_plurals(self.get_constituent_words(mention)[0]["pos"])

    def is_relative_pronoun(self, candidate, mention):

        #NP < (NP=m1 $.. (SBAR < (WHNP < WP|WDT=m2)))
        # M1 candidate M2 mention

        enclosing_np = self.get_syntactic_parent(candidate)

        upper = self.get_syntactic_parent(mention)
        while upper and (upper["type"] == self.graph_builder.root_type):
            if upper == enclosing_np:
                #TODO check path element
                #TODO m1 and m2 order
                return True
            upper = self.get_syntactic_parent(mention)
        return False
        # return set(filter(lambda X: X["tag"] in
        #                             constituent_tags.subordinated, mention.in_neighbours())).intersection(
        #     set(filter(lambda X: X["tag"] in
        #                          constituent_tags.subordinated, candidate.out_neighbours())))

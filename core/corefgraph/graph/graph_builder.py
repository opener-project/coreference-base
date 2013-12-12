# coding=utf-8
""" Base of graph creators to convert external linguistic knowledge into a graph usable by the system.
"""

from ..graph.xutils import GraphWrapper
from ..resources.tagset import ner_tags


class BaseGraphBuilder(object):
    """ THe Basic operations of text graph.
    """

    root_type = "ROOT"
    root_pos = "ROOT"
    root_label = "ROOT"
    root_edge_type = "ROOT"

    sentence_order_edge_type = "order"
    sentence_order_edge_label = "order"

    word_node_type = "word"
    word_edge_type = "form"

    entity_node_type = "entity"
    entity_edge_type = "refers"
    entity_edge_label = "refers"

    named_entity_node_type = "named_entity"
    named_entity_edge_type = "named_refers"
    named_entity_edge_label = "named_refers"

    syntactic_node_type = "constituent"
    syntactic_edge_type = "syntactic"
    syntactic_edge_label = "syntactic"
    syntactic_edge_value_branch = "contains"
    syntactic_edge_value_terminal = "terminal"

    head_edge_type = "is_head"
    head_word_edge_type = "is_head_word"

    dependency_node_type = "dependency"
    dependency_edge_type = "dependency"

    # Dependency edge Value is determined by parser


    word_count = 0
    sentence_count = 0
    document_count = 0

    def __init__(self):
        self.graph = None
        self.previous_sentence = None

    def new_graph(self):
        """ Create a new Graph and set all base properties for graph, vertex an edges.
        """
        graph = GraphWrapper.blank_graph()
        graph.graph['graph_builder'] = self
        return graph

    def set_graph(self, graph):
        """ Set the graph where this builders works
        @param graph: The graph target of this builder
        """
        self.graph = graph
        self.previous_sentence = None

    @staticmethod
    def set_ner(constituent, ner_type):
        """ Set the NER type to a constituent.
        @param constituent: The constituent
        @param ner_type: The ner type
        """
        constituent["ner"] = ner_type

    @staticmethod
    def get_ner(constituent):
        """ Get the NER type to a constituent.
        @param constituent: The constituent
        """
        return constituent.get("ner", ner_tags.no_ner)

    #Sentence Related
    def add_sentence(self, root_index, sentence_form, sentence_label, sentence_id):
        """ Create a new sentence in the graph. Also link it to the previous sentence.
        @param root_index: The index of the sentence
        @param sentence_form:
        @param sentence_label:
        @param sentence_id:
        @return: The sentence node
        """
        sentence_root_node = GraphWrapper.new_node(graph=self.graph,
                                                   node_type=self.root_type,
                                                   node_id=sentence_id,
                                                   form="{0}#{1}".format(self.root_label, sentence_form),
                                                   label="{0}#{1}".format(self.root_label, sentence_label),
                                                   ord=root_index,
                                                   tag=self.root_pos,
                                                   pos=self.root_pos,)
        if self.previous_sentence:
            self.link_sentences(self.previous_sentence, sentence_root_node)
        self.previous_sentence = sentence_root_node
        return sentence_root_node

    def link_sentences(self, sentence, next_sentence):
        """ link two consecutive sentences.
        @param sentence: first sentence of the union
        @param next_sentence: Second sentence of the union.
        """
        GraphWrapper.link(self.graph, sentence, next_sentence, self.sentence_order_edge_type,
                          1, self.sentence_order_edge_label)

    def get_next_sentence(self, sentence):
        """ Get the textual order next sentence
        @param sentence: The root of the base sentence
        @return: The next sentence
        """
        for sentence_node, next_sentence, relation_type in self.graph.out_edges(sentence["id"], keys=True):
            if relation_type == self.sentence_order_edge_type:
                return self.graph.node[next_sentence]
        return None

    def get_prev_sentence(self, sentence):
        """ Get the textual order previous sentence
        @param sentence: The root of the base sentence
        @return: The previous sentence
        """
        for prev_sentence, sentence_node, relation_type in self.graph.in_edges(sentence["id"], keys=True):
            if relation_type == self.sentence_order_edge_type:
                return self.graph.node[prev_sentence]
        return None

    def get_all_sentences(self, graph):
        """ Get all the sentences of the graph
        @param graph: The source graph
        @return: A list of sentences
        """
        return GraphWrapper.get_all_node_by_type(graph=graph, node_type=self.root_type)

    def same_sentence(self, element_a, element_b):
        """ Check if the nodes are in the same sentence

        @param element_a: Word, constituent or Named entity
        @param element_b: Word, constituent or Named entity
        """
        root_a = self.get_root(element_a)
        root_b = self.get_root(element_b)

        return root_a == root_b

    def sentence_distance(self, element_a, element_b):
        """ Get the distance between the sentences of 2 nodes( 0 for same sentence nodes).
        The distance is always a positive number.

        @param element_a: Word, constituent or Named entity
        @param element_b: Word, constituent or Named entity
        """
        root_a = self.get_root(element_a)
        root_b = self.get_root(element_b)
        return abs(root_a["sentence_order"] - root_b["sentence_order"])

    def get_sentence_words(self, sentence):
        """Get the (Sorted)words contained in a sentence.

         This method not traverse the syntactic tree, used the root direct links. NOT USE WITH CONSTITUENT.
        :param sentence: the root node of the sentence
        """
        return sorted(GraphWrapper.get_out_neighbours_by_relation_type(
            graph=self.graph, node=sentence, relation_type=self.word_edge_type),
            key=lambda y: y["ord"])

    #Correference
    def add_entity(self, entity_id, mentions, label=None):
        """ Creates a entity with the identification provided and link to all the mentions passed.

        :param label: Optional label for the mention.
        :param mentions: List of mentions that forms the entity.
        :param entity_id: identifier assigned to the mention.
        """
        graph = self.graph
        # Create the node that links all mentions as an entity.
        new_node = GraphWrapper.new_node(graph=graph,
                                         node_type=self.entity_node_type,
                                         node_id=entity_id,
                                         label=label
                                         )
        # Mention lis is a list of mention node identifiers
        for mention in mentions:
            GraphWrapper.link(self.graph, entity_id, mention, self.entity_edge_type, label=self.entity_edge_label)
        return new_node

    def get_all_entities(self, graph):
        """ Get all entities of the graph

        @param graph: The source graph
        @return: A list of entities
        """
        return GraphWrapper.get_all_node_by_type(graph=graph, node_type=self.entity_node_type)

    def get_all_entity_mentions(self, entity):
        """ Get mentions of a entity
        @param entity: The source entity
        @return: A list of mentions(elements)
        """
        return GraphWrapper.get_out_neighbours_by_relation_type(
            graph=self.graph, node=entity, relation_type=self.entity_edge_type)

    #Named entities
    def add_named_entity(self, entity_type, entity_id, label):
        """Creates a named entity into the graph.
        @param label: A label for representation uses.
        @param entity_id: The ID of the entity in the graph
        @param entity_type: The type of the NER
        """
        new_entity = GraphWrapper.new_node(graph=self.graph,
                                           node_type=self.named_entity_node_type,
                                           node_id=entity_id,
                                           label=label,
                                           ner=entity_type,
                                           tag=entity_type,
                                           )
        return new_entity

    def add_mention_of_named_entity(self, sentence, mention):
        """ Add a mention of an Named Entity.
        @param sentence:
        @param mention:
        @return:
        """
        GraphWrapper.link(graph=self.graph, origin=sentence, target=mention, link_type=self.named_entity_edge_type,
                          label=self.named_entity_edge_label)

    def get_sentence_named_entities(self, root):
        """Get the (Sorted)named entities contained in a sentence.

         This method not traverse the syntactic tree, used the root direct links. NOT USE WITH CONSTITUENT.
        :param root: the root of the sentence
        """
        return sorted(GraphWrapper.get_out_neighbours_by_relation_type(
            graph=self.graph, node=root, relation_type=self.named_entity_edge_type),
            key=lambda y: y["ord"])

    # Constituents
    def add_constituent(self, node_id, sentence, tag, order, label=None):
        """ Add a new constituent to the graph.
        @param node_id: The unique id in the graph
        @param sentence: The sentence Root
        @param tag: The tag of the constituent
        @param order: The order of the constituent
        @param label: A label for representation proposes
        @return: The constituent node
        """
        new_node = GraphWrapper.new_node(graph=self.graph,
                                         node_type=self.syntactic_node_type,
                                         node_id=node_id,
                                         tag=tag,
                                         label=label or tag,
                                         ord=order
                                         )
        self.link_root(sentence, new_node)
        return new_node

    # Words
    def add_word(self, form, node_id, label, lemma, pos, order, sentence=None, begin=-1, end=-1):
        """ Add a word into the graph. Also link it into its sentence
        @param form: The form of the word as it appears in the text.
        @param node_id: The unique id of the node
        @param label: The label of the word, for representative usage
        @param lemma: The lemma of the word
        @param pos: The Part of Speech of the word
        @param order:
        @param sentence:
        @param begin:
        @param end:
        @return:
        """
        word_node = GraphWrapper.new_node(
            graph=self.graph,
            node_type=self.word_node_type,
            node_id=node_id,
            form=form,
            label=label,
            pos=pos,
            lemma=lemma,
            begin=begin,
            end=end,
            ord=order,
            tag="WORD")
        if sentence:
            self.link_word(sentence=sentence, word=word_node)
            self.link_root(sentence=sentence, element=word_node)
        return word_node

    def link_word(self, sentence, word):
        """ Link a word with the sentence where it appears. Also make a root link.
        @param sentence: The sentence root node
        @param word: The word node
        """
        GraphWrapper.link(graph=self.graph, origin=sentence, target=word, link_type=self.word_edge_type)

    def get_words(self, element):
        """ Get the words(sorted in textual order) of the constituent.

        If constituent is a word, returns the words in a list.

        :param element: Word, constituent or Named entity
        """
        if element["type"] == self.word_node_type:
            return [element]
        words = GraphWrapper.get_out_neighbours_by_relation_type(self.graph, element, relation_type=self.word_edge_type)
        return sorted(words, key=lambda y: y["ord"])

    def remove(self, element):
        """ Remove the element from the graph
        @param element: The element to remove
        """
        GraphWrapper.remove(graph=self.graph, element=element)

    def unlink(self, origin, target):
        """ Break all link between a nodes. Only in one direction.
        @param origin: The origin node of the links
        @param target: The target node of the links
        """
        GraphWrapper.unlink(graph=self.graph, origin=origin, target=target)

    # Dependency
    def link_dependency(self, dependency_from, dependency_to, dependency_type):
        """ Add a dependency relation to the graph. Remember that dependency relations are down to top.
        @param dependency_from: The origin of the link
        @param dependency_to: The target of the link
        @param dependency_type: The value of the link
        """
        GraphWrapper.link(graph=self.graph, origin=dependency_from, target=dependency_to,
                          link_type=self.dependency_edge_type, value=dependency_type,
                          weight=1, label=self.dependency_edge_type + "_" + dependency_type)

    def get_dependant_words(self, word):
        """ Get all words that depend on the word and the dependency type.
        @param word: The word where the dependency starts
        """
        children = GraphWrapper.get_out_neighbours_by_relation_type(
            node=word, relation_type=self.dependency_edge_type, graph=self.graph, key=True)
        return children

    def get_governor_words(self, word):
        """ Get all words that rules a dependency link with the word and the dependency type.
        @param word: The word where the dependency ends
        """
        children = GraphWrapper.get_in_neighbours_by_relation_type(
            node=word, relation_type=self.dependency_edge_type, graph=self.graph, key=True)
        return children

    # Syntax
    def link_root(self, sentence, element):
        """ Link a word with the sentence where it appears
        @param sentence: The sentence root node
        @param element: The element
        """
        GraphWrapper.link(graph=self.graph, origin=sentence, target=element, link_type=self.root_edge_type)

    def link_syntax_non_terminal(self, parent, child):
        """ Link a non-terminal(constituent) to the constituent. Also link the constituent child word with the parent
        @param parent: The parent constituent
        @param child: The child constituent
        """
        for word in self.get_words(child):
            self.link_word(parent, word)

        GraphWrapper.link(graph=self.graph, origin=parent, target=child,
                          link_type=self.syntactic_edge_type, value=self.syntactic_edge_value_branch,
                          label=self.syntactic_edge_label + "_" + self.syntactic_edge_value_branch)

    def link_syntax_terminal(self, parent, terminal):
        """  Link a word to a constituent. Also add the word to
        @param parent:
        @param terminal:
        @return:
        """
        self.link_word(parent, terminal)
        GraphWrapper.link(graph=self.graph, origin=parent, target=terminal,
                          link_type=self.syntactic_edge_type, value=self.syntactic_edge_value_terminal,
                          weight=1, label=self.syntactic_edge_type + "_" + self.syntactic_edge_value_terminal)

    def set_head_word(self, element, head_word):
        """Set the head word of the element.

        @param element: Word, constituent or Named entity
        @param head_word: The word that is the head word
        """
        if head_word["type"] != self.word_node_type:
            raise Exception("No word as head word")
        GraphWrapper.link(self.graph, element, head_word, self.head_word_edge_type)

    def get_head_word(self, element):
        """ Get the head word. The word that is in the end of heads chain.
        @param element: Word, constituent or Named entity
        @return: The head word
        """
        if element["type"] == self.word_node_type:
            return element
        head = GraphWrapper.get_out_neighbour_by_relation_type(self.graph, element, self.head_word_edge_type)
        if head is None:
            head = self.get_words(element)[-1]
        return head


    def set_head(self, parent, head):
        """ Set a child as parent head and inverse inherit some values.
        @param parent: The parent constituent
        @param head: The child constituent or word
        """
        # Inverse inherit

        head[self.head_edge_type] = True

        # link
        self.set_head_word(parent, self.get_head_word(head))
        GraphWrapper.link(self.graph, parent, head, self.head_edge_type)

    def get_head(self, element):
        """Get the head of the element. If a word id passed by error the word itself is returned.
        @param element: Word, constituent or Named entity
        """
        if element["type"] == self.word_node_type:
            return element
        return GraphWrapper.get_out_neighbour_by_relation_type(
            graph=self.graph, node=element, relation_type=self.head_edge_type)

    def is_head(self, element):
        """ Determines if the constituent is head or its parent.
        @param element: The constituent to check
        @return: True of False
        """
        return self.head_edge_type in element and element[self.head_edge_type]

    # Syntactical navigation
    def get_root(self, element):
        """Get the sentence of the element

        :param element: The constituent or word whose parent is wanted.
        """
        if "constituent" in element:
            element = element["constituent"]
        return GraphWrapper.get_in_neighbour_by_relation_type(self.graph, element, self.root_edge_type)

    @staticmethod
    def is_inside(element_a_span, element_b_span):
        """Is m1 inside m2?
        @param element_a_span: Word, constituent or Named entity span
        @param element_b_span: Word, constituent or Named entity span
        """
        return (element_a_span[0] >= element_b_span[0]) and (element_a_span[1] <= element_b_span[1])

    def get_syntactic_children(self, element):
        """Get all the syntactical children of a element.

        :param element: The Word, constituent or Named entity whose children are wanted.
        """
        return GraphWrapper.get_out_neighbours_by_relation_type(
            graph=self.graph, node=element, relation_type=self.syntactic_edge_type)

    def get_syntactic_parent(self, element):
        """Return the syntactic parent of the node(constituent or word).

        :param element: The Word, constituent or Named entity whose parent is wanted.
        """
        if "constituent" in element:
            element = element["constituent"]

        return GraphWrapper.get_in_neighbour_by_relation_type(self.graph, element, self.syntactic_edge_type)

    def get_syntactic_sibling(self, element):
        """ Get the sibling  sons of the same parent of a syntactic node.

        @param element: Word, constituent or Named entity
        """
        if "constituent" in element:
            element = element["constituent"]
        syntactic_father = self.get_syntactic_parent(element)
        siblings = self.get_syntactic_children(syntactic_father)
        siblings.sort(key=lambda x: x["span"])
        return siblings

    def show_graph(self):
        """ Show a windows with the graph
        """
        GraphWrapper.show_graph(graph=self.graph)

    # Statistic propose
    def statistics_word_up(self):
        """  Add one to the word counter
        """
        self.__class__.word_count += 1

    def statistics_sentence_up(self):
        """  Add one to the sentence counter
        """
        self.__class__.sentence_count += 1

    def statistics_document_up(self):
        """  Add one to the document counter
        """
        self.__class__.document_count += 1

    @classmethod
    def get_stats(cls):
        """ Get the word sentence and document stats

        @return: a tuple with word, sentence and document count
        """
        return cls.word_count, cls.sentence_count, cls.document_count
    # End of statistic

    @classmethod
    def get_compose_id(cls, sentence_namespace, word_id, separator="_"):
        """ Generate a string id
        @param sentence_namespace: The base name for the sentence.
        @param word_id: The id of the word
        @param separator: A separator between sentence and word
        @return:
        """
        return "{1}{0}{2}".format(separator, sentence_namespace, word_id)

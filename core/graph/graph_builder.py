# Base of graph creators to convert external linguistic knowledge into a grpah usable by the system.

from graph_tool.all import GraphView
from graph.utils import GraphWrapper


class BaseGraphBuilder():

    neutral_named_entity_mark = "o"

    root_type = "ROOT"
    root_pos = "ROOT"
    root_label = "ROOT"

    word_node_type = "word"
    word_edge_type = "form"

    entity_node_type = "entity"
    entity_edge_type = "refers"
    entity_edge_label = "refers"

    named_entity_node_type = "named_entity"
    named_entity_edge_type = "named_refers"
    named_entity_edge_label = "named_refers"

    syntactic_node_type = "chunk"
    syntactic_edge_type = "syntactic"
    syntactic_edge_label = "syntactic"
    syntactic_edge_value_chunk = "contains"
    syntactic_edge_value_terminal = "terminal"

    dependency_node_type = "dependency"
    dependency_edge_type = "dependency"
    # Dependency edge Value is determined by parser

    color = {word_node_type: 'tomato',
             'chunk': 'blue',
             'root': 'purple',
             'entity': 'pink',
             'named_entity': 'green'}
    shape = {word_node_type: 'box',
             'chunk': 'box',
             'root': 'box',
             'entity': 'oval'}

    word_count = 0
    sentence_count = 0
    document_count = 0

    vertex_properties = {
        'id': "string",
        'type': "string",
        'form': "string",
        'pos': "string",
        'tag': "string",
        'head': "boolean",
        'ner': "string",
        'lemma': "string",
        'gender': "object",
        'animate': "object",
        'number': "object",
        'coreference': "vector<string>",
        'ord': "int64_t",
        'sentence_root': 'object',
        'begin': "int64_t",
        'end': "int64_t",
        'label': "string",
        'color': "string",
        'shape': "string"}

    edge_properties = {
        'type': "string",
        'value': "string",
        'weight': "int",
        'label': "string"}

    graph_properties = {
        'graph_builder': "object",
        'last-sentence': "int64_t"}

    def set_graph(self, graph):
        self.graph = graph

    def new_graph(self):
        """ Create a new Graph and set all base properties for graph, vertex an edges.
        """
        graph = GraphWrapper.blank_graph()
        GraphWrapper.define_properties(graph,
                                       vertex_properties=self.vertex_properties,
                                       edge_properties=self.edge_properties,
                                       graph_properties=self.graph_properties)
        GraphWrapper.set_properties(graph=graph, graph_properties={'graph_builder': self})
        return graph

    def get_node_property(self, name):
        return GraphWrapper.node_property(name=name, graph=self.graph)

    def get_graph_property_value(self, name):
        return GraphWrapper.get_graph_property(graph=self.graph, property_name=name)

    def set_graph_property_value(self, name, value):
        return GraphWrapper.set_graph_property(graph=self.graph, property_name=name, value=value)

    def set_head(self, node):
        node_head = GraphWrapper.node_property(name="head", graph=node.get_graph())
        node_head[node] = True

    def add_sentence(self, root_index, sentence_form, sentence_label, sentence_id):
        sentence_root_node = GraphWrapper.new_node(graph=self.graph,
                                                   type=self.root_type,
                                                   id=sentence_id,
                                                   form="{0}#{1}".format(self.root_label, sentence_form),
                                                   label="{0}#{1}".format(self.root_label, sentence_label),
                                                   ord=root_index,
                                                   tag=self.root_pos,
                                                   pos=self.root_pos,
                                                   color=self.color['root'],
                                                   shape=self.shape['root'],)
        return sentence_root_node

    def add_word(self, form, wid, label, lemma, ner, pos, head, sentence_root_node=None, begin=-1, end=-1):
        word_node = GraphWrapper.new_node(
            graph=self.graph,
            id=wid,
            form=form,
            label=label,
            pos=pos,
            ner=ner,
            type=self.word_node_type,
            lemma=lemma,
            head=head,
            color=self.color[self.word_node_type],
            shape=self.shape[self.word_node_type],
            begin=begin,
            end=end,
        )
        if sentence_root_node:
            self.link_word(sentence_root_node=sentence_root_node, word_node=word_node)
        return word_node

    def add_chunk(self, form, head, label, lemma, ner, tag):
        new_node = GraphWrapper.new_node(graph=self.graph,
                                         type=self.syntactic_node_type,
                                         tag=tag,
                                         form=form,
                                         label=label,
                                         ner=ner,
                                         lemma=lemma,
                                         head=head,
                                         color=self.color['chunk'],
                                         shape=self.shape['chunk'],
                                         )
        return new_node

    def cut_chunk(self, chunk, index, new_tag):
        graph = self.graph
        node_form = GraphWrapper.node_property("form", graph)
        node_head = GraphWrapper.node_property("head", graph)
        node_label = GraphWrapper.node_property("label", graph)
        # Create a new constituent to cover the Ner mention
        head = False
        form = ""
        new_constituent = self.add_chunk(form=form, head=head, label=form, lemma="", ner="O", tag=new_tag)
        for child in self.get_chunk_children(chunk)[:index + 1]:
            form += node_form[child]
            head = head or node_head[child]
            self.unlink(chunk, child)
            self.syntactic_terminal_link(parent_node=new_constituent, terminal_node=child)
        node_form[new_constituent] = form
        node_head[new_constituent] = head
        node_label[new_constituent] = form
        self.syntax_tree_link(new_constituent, chunk)

    def add_entity(self, mentions, label=None):
        graph = self.graph
        new_node = GraphWrapper.new_node(graph=graph,
                                         type=self.entity_node_type,
                                         color=self.color['entity'],
                                         shape=self.shape['entity'],
                                         label=label
                                         )
        for mention in mentions:
            GraphWrapper.link(self.graph, new_node, mention, self.entity_edge_type, label=self.entity_edge_label)
        return new_node

    def add_named_entity(self, entity_type, entity_id, label=None):
        new_entity = GraphWrapper.new_node(graph=self.graph,
                                           type=self.named_entity_node_type,
                                           color=self.color['named_entity'],
                                           shape=self.shape['entity'],
                                           label=label,
                                           tag=entity_type,
                                           id=entity_id,)
        return new_entity

    def add_named_mention(self, named_entity, mention):
        GraphWrapper.link(graph=self.graph, origin=named_entity, target=mention, node_type=self.named_entity_edge_type,
                          label=self.named_entity_edge_label)

    def unlink(self, parent, child):
        GraphWrapper.unlink(parent, child)

    def link_word(self, sentence_root_node, word_node):
        GraphWrapper.link(self.graph, sentence_root_node, word_node, self.word_edge_type, 1)

    def syntax_tree_link(self, child, parent):
        GraphWrapper.link(graph=self.graph, origin=parent, target=child,
                          node_type=self.syntactic_edge_type,
                          label=self.syntactic_edge_label)

    def syntactic_terminal_link(self, parent_node, terminal_node):
        GraphWrapper.link(graph=self.graph, origin=parent_node, target=terminal_node,
                          node_type=self.syntactic_edge_type, value=self.syntactic_edge_value_terminal,
                          weight=1, label=self.syntactic_edge_type + "_" + self.syntactic_edge_value_terminal)

    def show_graph(self):
        GraphWrapper.showGraph(graph=self.graph, vcolor='color', vshape="shape")

    # Statistic propose
    def statistics_word_up(self):
        self.__class__.word_count += 1

    def statistics_sentence_up(self):
        self.__class__.sentence_count += 1

    def statistics_document_up(self):
        self.__class__.document_count += 1

    @classmethod
    def get_stats(cls):
        return cls.word_count, cls.sentence_count, cls.document_count
    # End of statistic

    @classmethod
    def get_word_graph(cls, graph):
        """ A graph View that contains all vertex words of the text graph.
        """
        return GraphView(g=graph, vfilt=lambda v: graph.vertex_properties["type"][v] == cls.word_node_type)

    @classmethod
    def get_syntax_graph(cls, graph):
        """ A graph that contains all syntax related relations of the text graph.
        :param graph: the Graph where view come from.
        """
        return GraphView(g=graph, efilt=lambda e: graph.edge_properties["type"][e] == cls.syntactic_edge_type)

    @classmethod
    def get_referent_graph(cls, graph):
        """ A graph view that contains all referents of the text graph .
        """
        return GraphView(g=graph, vfilt=lambda v: graph.vertex_properties["type"][v] == "referent")

    @classmethod
    def get_navigable_graph(cls, graph):
        """ A graph that allow "navigate" thought accessibility relations.
        """
        GraphView(g=graph, reversed=True,
                  efilt=lambda e: graph.edge_properties["type"][e] in ("subordinated", "equal", "referent"))

    @classmethod
    def get_sentence_words(cls, root):
        return GraphWrapper.get_filtered_by_type_out_neighbours(node=root, relation_type=cls.word_edge_type)

    @classmethod
    def get_syntactic_parent(cls, root):
        parent_list = GraphWrapper.get_filtered_by_type_in_neighbours(node=root, relation_type=cls.syntactic_edge_type)
        if len(parent_list) > 0:
            return parent_list[0]
        else:
            return None

    @classmethod
    def get_constituent_words(cls, chunk):

        node_type = GraphWrapper.node_property(name="type", graph=chunk.get_graph())

        def __iterate__(syntax_chunk):
            for child in GraphWrapper.get_filtered_by_type_out_neighbours(syntax_chunk, cls.syntactic_edge_type):
                if node_type[child] == cls.word_node_type:
                    words.append(child)
                else:
                    __iterate__(child)
        # End of iteration
        if node_type[chunk] == cls.word_node_type:
            words = [chunk]
        else:
            words = []
            __iterate__(chunk)
        return words

    @classmethod
    def get_entity_mentions(cls, entity):
        return GraphWrapper.get_filtered_by_type_out_neighbours(node=entity, relation_type=cls.entity_edge_type)

    @classmethod
    def get_chunk_children(cls, chunk):
        return GraphWrapper.get_filtered_by_type_out_neighbours(node=chunk, relation_type=cls.syntactic_edge_type)

    @classmethod
    def get_chunk_head_word(cls, chunk):
        node_type = GraphWrapper.node_property(name="type", graph=chunk.get_graph())
        head = GraphWrapper.node_property(name="head", graph=chunk.get_graph())

        def __iterate__(syntax_chunk):
            for child in GraphWrapper.get_filtered_by_type_out_neighbours(node=syntax_chunk,
                                                                          relation_type= cls.syntactic_edge_type):
                if head[child]:
                    if node_type[child] == cls.word_node_type:
                        return child
                    else:
                        return __iterate__(child)
            return None
        if node_type[chunk] == cls.word_node_type:
                return chunk
        return __iterate__(chunk)

    @classmethod
    def get_chunk_head(cls, chunk):
        head = GraphWrapper.node_property(name="head", graph=chunk.get_graph())
        children = GraphWrapper.get_filtered_by_type_out_neighbours(node=chunk, relation_type=cls.syntactic_edge_type)
        if len(children) == 1:
            return children[0]
        for child in children:
            if head[child]:
                return child
        return None

    @classmethod
    def extract_all_roots(cls, graph):
        return GraphWrapper.get_all_vertex_by_type(graph=graph, vertex_type=cls.root_type)

    @classmethod
    def extract_entities(cls, graph):
        return GraphWrapper.get_all_vertex_by_type(graph=graph, vertex_type=cls.entity_node_type)

    @classmethod
    def get_compose_id(cls, sentenceNamespace, word_id, separator="_"):
        """ Generate a string id for the word based in their sentence and word numbers."""
        return "{1}{0}{2}".format(separator, sentenceNamespace, word_id)
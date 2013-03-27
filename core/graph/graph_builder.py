# change to the Stanford Corenlp Python bindings.

from graph_tool.all import GraphView

from graph.utils import GraphWrapper


class BaseGraphBuilder():

    root_type = "ROOT"
    root_pos = "ROOT"

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
        """ Create a new Graph and set all base properties.
        """
        graph = GraphWrapper.blank_graph()
        GraphWrapper.define_properties(graph,
                                       vertex_properties=self.vertex_properties,
                                       edge_properties=self.edge_properties,
                                       graph_properties=self.graph_properties)
        GraphWrapper.set_properties(graph=graph, graph_properties={'graph_builder': self})
        return graph

    def get_property(self, name):
        return GraphWrapper.node_property(name, self.graph)

    def add_sentence(self, graph, root_index, sentence_form, sentence_label, sentence_id):
        sentence_root_node = GraphWrapper.new_node(graph=graph,
                                                   type=self.root_type,
                                                   id=sentence_id,
                                                   form="ROOT#{0}".format(sentence_form),
                                                   label="ROOT#{0}".format(sentence_label),
                                                   ord=root_index,
                                                   tag=self.root_pos,
                                                   pos=self.root_pos,
                                                   color=self.color['root'],
                                                   shape=self.shape['root'],
        )
        return sentence_root_node

    def link_word(self, sentence_root_node, word_node):
        GraphWrapper.link(self.graph, sentence_root_node, word_node, self.word_edge_type, 1)

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

    def add_chunk(self, form, graph, head, label, lemma, ner, tag):
        new_node = GraphWrapper.new_node(graph,
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

    def add_entity(self, graph, mentions, log=None):
        new_node = GraphWrapper.new_node(graph,
                                         type=self.entity_node_type,
                                         color=self.color['entity'],
                                         shape=self.shape['entity'],
                                         label=log
                                         )
        for mention in mentions:
            GraphWrapper.link(self.graph, new_node, mention, self.entity_edge_type, label=self.entity_edge_label)
        return new_node

    def add_named_entity(self, graph, entity_type, entity_id, log=None):
        new_entity = GraphWrapper.new_node(graph,
                                           type=self.named_entity_node_type,
                                           color=self.color['named_entity'],
                                           shape=self.shape['entity'],
                                           label=log,
                                           tag=entity_type,
                                           id=entity_id,)
        return new_entity

    def add_named_mention(self, named_entity, mention):
        GraphWrapper.link(self.graph, named_entity, mention, self.named_entity_edge_type,
                          label=self.named_entity_edge_label)

    def syntax_tree_link(self, child, parent):
        GraphWrapper.link(self.graph, origin=parent, target=child,
                          node_type=self.syntactic_edge_type,
                          label=self.syntactic_edge_label)

    def syntactic_terminal_link(self, parent_node, terminal_node):
        GraphWrapper.link(self.graph, origin=parent_node, target=terminal_node,
                          node_type=self.syntactic_edge_type, value=self.syntactic_edge_value_terminal,
                          weight=1, label=self.syntactic_edge_type + "_" + self.syntactic_edge_value_terminal)

    @classmethod
    def get_stats(cls):
        return cls.word_count, cls.sentence_count, cls.document_count

    # Statistic propose
    def wordup(self):
        self.__class__.word_count += 1

    def sentenceup(self):
        self.__class__.sentence_count += 1

    def documentup(self):
        self.__class__.document_count += 1

    # End of statistic
    def show_graph(self):
        GraphWrapper.showGraph(self.graph, vcolor='color', vshape="shape")

    def set_head(self, node):
        node_head = GraphWrapper.node_property("head", node.get_graph())
        node_head[node] = True

    @classmethod
    def get_word_graph(cls, graph):
        """ A graph View that contains all vertex words of the text graph.
        """
        return GraphView(graph, vfilt=lambda v: graph.vertex_properties["type"][v] == cls.word_node_type)

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
        return GraphView(graph, vfilt=lambda v: graph.vertex_properties["type"][v] == "referent")

    @classmethod
    def get_navigable_graph(cls, graph):
        """ A graph that allow "navigate" thought accessibility relations.
        """
        GraphView(g=graph, reversed=True,
                  efilt=lambda e: graph.edge_properties["type"][e] in ("subordinated", "equal", "referent"))

    @classmethod
    def get_sentence_words(cls, root):
        return GraphWrapper.get_filtered_by_type_out_neighbours(root, cls.word_edge_type)

    @classmethod
    def get_syntactic_parent(cls, root):
        parent_list = GraphWrapper.get_filtered_by_type_in_neighbours(root, cls.syntactic_edge_type)
        if len(parent_list) > 0:
            return parent_list[0]
        else:
            return None

    @classmethod
    def get_constituent_words(cls, chunk):

        node_type = GraphWrapper.node_property("type", chunk.get_graph())

        def __iterate__(syntax_chunk):
            for child in GraphWrapper.get_filtered_by_type_out_neighbours(syntax_chunk, cls.syntactic_edge_type):
                if node_type[child] == cls.word_node_type:
                    words.append(child)
                else:
                    __iterate__(child)
        if node_type[chunk] == cls.word_node_type:
            words = [chunk]
        else:
            words = []
            __iterate__(chunk)
        return words

    @classmethod
    def get_entity_mentions(cls, entity):
        return GraphWrapper.get_filtered_by_type_out_neighbours(entity, cls.entity_edge_type)

    @classmethod
    def get_chunk_children(cls, chunk):
        return GraphWrapper.get_filtered_by_type_out_neighbours(chunk, cls.syntactic_edge_type)

    @classmethod
    def get_chunk_head_word(cls, chunk):
        node_type = GraphWrapper.node_property("type", chunk.get_graph())
        head = GraphWrapper.node_property("head", chunk.get_graph())

        def __iterate__(syntax_chunk):
            for child in GraphWrapper.get_filtered_by_type_out_neighbours(syntax_chunk, cls.syntactic_edge_type):
                if head[child]:
                    if node_type[child] == cls.word_node_type:
                        return child
                    else:
                        return __iterate__(child)
            return None
        if head[chunk]:
            if node_type[chunk] == cls.word_node_type:
                return chunk
        return __iterate__(chunk)

    @classmethod
    def get_chunk_head(cls, chunk):
        head = GraphWrapper.node_property("head", chunk.get_graph())
        children = GraphWrapper.get_filtered_by_type_out_neighbours(chunk, cls.syntactic_edge_type)
        if len(children) == 1:
            return children[0]
        for child in children:
            if head[child]:
                return child
        return None

    @classmethod
    def extract_all_roots(cls, graph):
        return GraphWrapper.get_all_vertex_by_type(graph, cls.root_type)

    @classmethod
    def extract_entities(cls, graph):
        return GraphWrapper.get_all_vertex_by_type(graph, cls.entity_node_type)




    @classmethod
    def get_compose_id(cls, sentenceNamespace, word_id, separator="_"):
        """ Generate a string id for the word based in their sentence and word numbers."""
        return "{1}{0}{2}".format(separator, sentenceNamespace, word_id)



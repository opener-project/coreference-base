# Base of graph creators to convert external linguistic knowledge into a grpah usable by the system.

from graph.xutils import GraphWrapper


class BaseGraphBuilder():
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
    syntactic_edge_value_branch = "contains"
    syntactic_edge_value_terminal = "terminal"

    head_link = "is_head"

    dependency_node_type = "dependency"
    dependency_edge_type = "dependency"

    # Dependency edge Value is determined by parser
    color = {word_node_type: 'tomato',
             'chunk': 'lightblue',
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
        'form': "object",
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
        'label': "object",
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
        graph.graph['graph_builder'] = self
        return graph

    def set_head(self, parent, node):
        node["head"] = True
        GraphWrapper.link(self.graph, parent, node, self.head_link)

    def add_sentence(self, root_index, sentence_form, sentence_label, sentence_id):
        sentence_root_node = GraphWrapper.new_node(graph=self.graph,
                                                   node_type=self.root_type,
                                                   node_id=sentence_id,
                                                   form="{0}#{1}".format(self.root_label, sentence_form),
                                                   label="{0}#{1}".format(self.root_label, sentence_label),
                                                   ord=root_index,
                                                   tag=self.root_pos,
                                                   pos=self.root_pos,
                                                   color=self.color['root'],
                                                   shape=self.shape['root'], )
        return sentence_root_node

    def add_word(self, form, wid, label, lemma, ner, pos, head, order, sentence_root_node=None, begin=-1, end=-1):
        word_node = GraphWrapper.new_node(
            graph=self.graph,
            node_id=wid,
            form=form,
            label=label,
            pos=pos,
            ner=ner,
            node_type=self.word_node_type,
            lemma=lemma,
            head=head,
            color=self.color[self.word_node_type],
            shape=self.shape[self.word_node_type],
            begin=begin,
            end=end,
            ord=order
            )
        if sentence_root_node:
            self.link_word(sentence_root_node=sentence_root_node, word_node=word_node)
        return word_node

    def add_constituent(self, node_id, form, head, root, label, lemma, ner, tag, order):
        new_node = GraphWrapper.new_node(graph=self.graph,
                                         node_type=self.syntactic_node_type,
                                         node_id=node_id,
                                         tag=tag,
                                         form=form,
                                         label=label,
                                         ner=ner,
                                         lemma=lemma,
                                         head=head,
                                         root=root,
                                         color=self.color['chunk'],
                                         shape=self.shape['chunk'],
                                         ord=order
                                         )
        return new_node

    def add_entity(self, entity_id, mentions, label=None):
        """ Creates a entity wiht the identificator provided and link to all the mentions passed.


        :param label: Optional label for the mention.
        :param mentions: List of mentions that forms the entity.
        :param entity_id: Idientifier assigned to the mention.
        """
        graph = self.graph
        # Create the node that links all mentions as an entity.
        new_node = GraphWrapper.new_node(graph=graph,
                                         node_type=self.entity_node_type,
                                         node_id=entity_id,
                                         color=self.color['entity'],
                                         shape=self.shape['entity'],
                                         label=label
                                         )
        # Mention lis is a list of mention node identifiers
        for mention in mentions:
            GraphWrapper.link(self.graph, entity_id, mention, self.entity_edge_type, label=self.entity_edge_label)
        return new_node

    def add_named_entity(self, entity_type, entity_id, label):
        new_entity = GraphWrapper.new_node(graph=self.graph,
                                           node_type=self.named_entity_node_type,
                                           node_id=entity_id,
                                           color=self.color['named_entity'],
                                           shape=self.shape['entity'],
                                           label=label,
                                           ner=entity_type,
                                           tag=entity_type,
                                           )
        return new_entity

    def add_named_mention(self, root, mention):
        GraphWrapper.link(graph=self.graph, origin=root, target=mention, link_type=self.named_entity_edge_type,
                          label=self.named_entity_edge_label)

    def unlink(self, parent, child):
        GraphWrapper.unlink(origin=parent, target=child)

    def link_word(self, sentence_root_node, word_node):
        word_node["root"] = sentence_root_node
        GraphWrapper.link(graph=self.graph, origin=sentence_root_node, target=word_node, link_type=self.word_edge_type)

    def syntax_tree_link(self, parent, child):
        GraphWrapper.link(graph=self.graph, origin=parent, target=child,
                          link_type=self.syntactic_edge_type, value=self.syntactic_edge_value_branch,
                          label=self.syntactic_edge_label + "_" + self.syntactic_edge_value_branch)

    def syntactic_terminal_link(self, parent_node, terminal_node):
        GraphWrapper.link(graph=self.graph, origin=parent_node, target=terminal_node,
                          link_type=self.syntactic_edge_type, value=self.syntactic_edge_value_terminal,
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

    def get_entity_mentions(self, entity):
        return GraphWrapper.get_filtered_by_type_out_neighbours(
            graph=self.graph, node=entity, relation_type=self.entity_edge_type)

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
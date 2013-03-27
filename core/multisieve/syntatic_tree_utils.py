__author__ = 'nasgar'
from graph.utils import GraphWrapper
import dictionaries


class SyntacticTreeUtils():
    def __init__(self, graph):
        self.graph = graph
        self.graph_builder = GraphWrapper.get_graph_property(self.graph, 'graph_builder')
        self.mention_tag = GraphWrapper.node_property("tag", self.graph)
        self.mention_form = GraphWrapper.node_property("form", self.graph)
        self.relation_type = GraphWrapper.edge_property("type", self.graph)

    def same_sentence(self, nodeA, nodeB):
        return GraphWrapper.get_node_property(
            nodeA, "sentence_root", self.graph) == GraphWrapper.get_node_property(nodeB, "sentence_root", self.graph)

    def sentence_distance(self, nodeA, nodeB):
        root_a = GraphWrapper.get_node_property(
            nodeA, "sentence_root", self.graph)
        root_b = GraphWrapper.get_node_property(nodeB, "sentence_root", self.graph)
        return abs(GraphWrapper.get_node_property(root_a, "ord") - GraphWrapper.get_node_property(root_b, "ord"))

    def get_sibling(self, mention):
        syntactic_father = [relation.source()
                            for relation in mention.in_edges() if self.relation_type[relation] == "syntactic"]
        return [relation.target()
                for relation in syntactic_father[0].out_edges() if self.relation_type[relation] == "syntactic"]

    def is_appositive_construction(self, mention):
        siblings = self.get_sibling(mention)

        for sibling in siblings:
            if self.mention_tag[sibling] == dictionaries.conjuntion_tag:
                return False

        if len(siblings) == 3:
            return self.mention_tag[siblings[0]] == dictionaries.noun_phrase_tag and \
                self.mention_form[siblings[1]] == ","
        elif len(siblings) > 3:
            return self.mention_tag[siblings[0]] == dictionaries.noun_phrase_tag and \
                self.mention_form[siblings[1]] == "," and \
                self.mention_form[siblings[3]] == ","
        else:
            return False

    def is_predicative_nominative(self, mention):
        siblings = self.get_sibling(mention)
        mention_index = siblings.index(mention)
        if mention_index > 0 and \
                self.mention_form[siblings[mention_index - 1]].split()[-1] in dictionaries.copulative_verbs:
            return True
        return False

    def is_relative_pronoun(self, candidate, mention):
        return set(filter(lambda X: self.mention_tag[X] in
                       dictionaries.subordinated_clause_tag, mention.in_neighbours())).intersection(
                set(filter(lambda X: self.mention_tag[X] in
                    dictionaries.subordinated_clause_tag, candidate.out_neighbours())))

    def get_syntactic_parent(self, mention):
        return  self.graph_builder.get_syntactic_parent(mention)

    def get_chunk_words(self, mention):
        return self.graph_builder.get_constituent_words(mention)

    def get_chunk_head_word(self, mention):
        return self.graph_builder.get_chunk_head_word(mention)
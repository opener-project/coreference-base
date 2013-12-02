# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ..graph.graph_builder import BaseGraphBuilder

import logging

#WARNING This class is unmaintained


class OntonotesGraphBuilder(BaseGraphBuilder):

    def __init__(self, corpus, logger=logging.getLogger("OntonotesGraphBuilder")):
        """ Extract form the ontonotes the document info and puts into graph form
        """
        self.corpus = corpus
        self.logger = logger

    def preprocess_sentences(self, graph, document):
        self.graph = graph

    def process_sentence(self, graph, sentence, root_index, sentence_namespace=None):
        """Add to the graph the morphological, syntactical and dependency info contained in the sentence.

        sentence: the sentence to parse
        sentenceNamespace:: prefix added to all nodes ID strings.
        separator: character or string used for create the nodes ID string.
        """
        self.graph = graph
        sentence_id = sentence.id
        # Sentence Root
        sentence_root_label = "ROOT#" + sentence_id
        sentence_root_form = sentence.get_plain_sentence()
        sentence_root_node = self.add_sentence(root_index, sentence_root_form, sentence_root_label, sentence_id)
        # Dependency
        # Create Edges for each dependency
        #self.parse_dependency(graph, sentence_root_node, sentence, sentenceNamespace, separator)

        self.parse_syntax(sentence, sentence_root_node)
        # Return the generated context graph
        self.statistics_sentence_up()
        return sentence_root_node

    def parse_word(self, word_leaf, sentence_root_node):
        """Parse and add a word tho the sentence root"""
        word_id = word_leaf.id
        form = word_leaf.word
        label = "|".join((word_leaf.id, word_leaf.part_of_speech, word_leaf.word))
        ner = word_leaf.named_entity or "o"
        pos = word_leaf.part_of_speech
        lemma = word_leaf.lemma
        word_node = self.add_word(form=form, node_id=word_id, label=label, lemma=lemma, pos=pos,
                                  sentence=sentence_root_node)
        word_node["ber"] = ner
        self.statistics_word_up()
        return word_node

    def parse_chunk(self, chunk):
        """Parse a chunk an return the chunk node"""
        # Create the chunk element
        #TODO mark head
        tag = chunk.tag
        form = chunk.get_plain_sentence()
        label = chunk.tag
        ner = chunk.named_entity
        lemma = chunk.get_plain_sentence()
        head = False
        new_chunk = self.add_chunk(form=form, head=head, label=label, lemma=lemma, ner=ner, tag=tag)
        return new_chunk

    def parse_syntax(self, sentence, sentence_root_node):
        """ Parse the syntax tree to introduce syntactical and morphological info into the graph.
        The tree is traversed in DSF.
        The word span is calculated with the word and chunk length.
        """
        char_offset = 0
        node_begin = self.get_node_property("begin")
        node_end = self.get_node_property("end")

        def iterate( chunk, parent):
            """The iteration function used tho traverse the parse tree."""
            # The tree node is a chunk or a word
            if chunk.is_leaf():
                new_node = self.parse_word(chunk, sentence_root_node)
            else:
                new_node = self.parse_chunk(chunk)
                for child in chunk.children:
                    iterate(child, new_node)
            # In any case
            begin = char_offset + chunk.start
            end = char_offset + chunk.end
            node_begin[new_node] = begin
            node_end[new_node] = end
            self.link_syntax_non_terminal(parent, new_node)
            return end
        # End Iteration
        for child in sentence.children:
            # Offset is end of the last chunk/word
            char_offset = iterate(child, sentence_root_node)
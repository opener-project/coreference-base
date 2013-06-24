from graph.graph_builder import BaseGraphBuilder
from graph.utils import GraphWrapper
from output.basewriter import BaseDocument

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class ConllDocument(BaseDocument):
    """ Store the results into a plain text evaluable by the Conll script
    """
    def store(self, graph):
        """ Stores the graph content in Conll format into the object file.
        :param graph: The graph is going to be stored.
        """
        self.word_id = GraphWrapper.node_property("id", graph)
        self.pos = GraphWrapper.node_property("pos", graph)
        self.form = GraphWrapper.node_property("form", graph)
        self.ner = GraphWrapper.node_property("ner", graph)
        self.coreference = GraphWrapper.node_property("coreference", graph)
        self.file.write("#begin document {0}; part {1}".format(self.document_id, 0))
        sentences_roots = BaseGraphBuilder.extract_all_roots(graph)
        #widgets = ['Storing document {0}: '.format(self.id), Fraction()]
        #pbar = ProgressBar(widgets=widgets, maxval=len(sentences_roots), force_update=True).start()
        for index, root in enumerate(sentences_roots):
            self.file.write("\n")
            for word in BaseGraphBuilder.get_sentence_words(root):
                self.file.write(self.word_to_cnll(word))
            #pbar.update(index + 1)
        #pbar.finish()
        self.file.write("#end document".format(self.document_id, 0))

    def word_to_cnll(self, word):
        """A word in ConLL is represented with a line of text that is composed by a list of features separated by tabs.
        :param word: The word that is going to be parsed.
        """
        features = [
            self.word_id[word].split("_")[0],
            self.pos[word],
            self.form[word],
            self.ner[word],
            "|".join(self.coreference[word]),
            "\n"]
        return "\t".join(features)
# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from .basewriter import BaseDocument


class ConllDocument(BaseDocument):
    """ Store the results into a plain text evaluable by the Conll script
    """

    def store(self, graph, document_id, part_id):
        """ Stores the graph content in Conll format into the object file.
        :param graph: The graph is going to be stored.
        """
        self.graph_builder = graph.graph["graph_builder"]
        for coref_index, entity in enumerate(self.graph_builder.get_all_entities(graph), 1):
            self.annotate_mentions(self.graph_builder.get_all_entity_mentions(entity), coref_index)
            print coref_index, entity, [x["id"] for x in self.graph_builder.get_all_entity_mentions(entity)]


        self.file.write("#begin document ({0}); part {1}".format(document_id, part_id))
        sentences_roots = self.graph_builder.get_all_sentences(graph)
        for sentence_index, root in enumerate(sentences_roots):
            self.file.write("\n")
            for word_index, word in enumerate(self.graph_builder.get_sentence_words(root)):
                self.file.write(self.word_to_cnll(word, document_id, str(int(part_id)), str(sentence_index), str(word_index)))
        self.file.write("\n#end document\n")

    def annotate_mentions(self, mentions, cluster_index):
        for mention in mentions:
            # For each mention word assign the cluster id to cluster attribute
            # and mark start and end with '(' and ')'
            terms = self.graph_builder.get_words(mention)
            # Valid for 0, 1 and n list sides
            if terms:
                if len(terms) == 1:
                    self._mark_coreference(terms[0], "({0})".format(cluster_index))
                else:
                    self._mark_coreference(terms[0], "({0}".format(cluster_index))
                    self._mark_coreference(terms[-1], "{0})".format(cluster_index))

    @staticmethod
    def _mark_coreference(word, coreference_string):
        """ Append to a word a coreference string
        @param word: The word that forms part of a mention
        @param coreference_string: The coreference string
        """
        if not "coreference" in word:
            word["coreference"] = [coreference_string]
        else:
            word["coreference"].append(coreference_string)

    def word_to_cnll(self, word,document_id, part_id, sentence_id, word_id):
        """A word in ConLL is represented with a line of text that is composed by a list of features separated by tabs.
        :param word: The word that is going to be parsed.
        """
        features = [
            document_id,
            part_id,
            word_id,
            word["form"],
            word["pos"],
            word["lemma"],
            "X",
            "-",  "-", "-", "-", "-",
        ]

        if "coreference" in word:
            features.append("|".join(word["coreference"]))
        else:
            features.append("-")

        return "   ".join(features) + "\n"

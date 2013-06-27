from output.basewriter import BaseDocument
from pykaf.kaf import KafDocument as Kaf
import time

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class KafDocument(BaseDocument):
    """ Store the document in a KAF format(2.1).
    """
    def store(self, graph, encoding, language=None, version=None, linguistic_parsers=(),
              time_stamp=time.strftime("%y-%m-%dT%H:%M:%S")):
        """ Store the graph in a string and return it.
        :param graph: the graph to be stored.
        :param language: The language code inserted into the kaf file
        """
        graphBuilder = graph.graph["graph_builder"]
        graph_utils = graph.graph["utils"]

        # Check if graph contains a pre generated kaf
        try:
            previous_kaf = graph.graph["kaf"]
        except KeyError:
            previous_kaf = None

        if previous_kaf:
            kaf_document = previous_kaf
            for lp_name, lp_version, lp_layer, time_stamp in linguistic_parsers:
                kaf_document.add_linguistic_processors(layer=lp_layer, name=lp_name, version=lp_version,
                                                       time_stamp=time_stamp)
            for coref_index, entity in enumerate(graphBuilder.extract_entities(graph), 1):
                references = [([word["id"].split("#")[0]
                                for word in graph_utils.get_constituent_words(mention)], mention["form"])
                                    for mention in graphBuilder.get_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)

        else:
            kaf_document = Kaf(language=language, version=version)

            words_graphs = graphBuilder.get_word_graph(graph)

            for lp_name, lp_version, lp_layer in linguistic_parsers:
                kaf_document.add_linguistic_processors(layer=lp_layer, name=lp_name, version=lp_version,
                                                       time_stamp=time_stamp)

            word_index = 1
            terms_ids = dict()

            for (term_index, graph_word) in enumerate(words_graphs.vertices(), 1):
                kaf_words = graph_word["form"].split(" ")
                words_ids = []
                for word in kaf_words:
                    word_id = "w{0}".format(word_index)
                    kaf_document.add_word(word, word_id, lemma=word["lemma"])
                    words_ids.append(word_id)
                    word_index += 1
                term_id = "t{0}".format(term_index)
                terms_ids[graph_word] = term_id
                kaf_document.add_term(tid=term_id, pos=graph_word["pos"], words=words_ids)

            for coref_index, entity in enumerate(graphBuilder.extract_entities(graph), 1):
                references = [([terms_ids[word]
                                for word in graphBuilder.get_constituent_words(mention)], mention["form"])
                              for mention in graphBuilder.get_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)

        kaf_document.write(self.file, encoding=encoding)
        return kaf_document

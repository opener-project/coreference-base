# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from .basewriter import BaseDocument

from pynaf import NAFDocument as Kaf
import time


class KafDocument(BaseDocument):
    """ Store the document in a KAF format(2.1).
    """
    time_format = "%Y-%m-%dT%H:%M:%S"

    def store(self, graph, encoding, language=None, version=None, linguistic_parsers=(),
              time_stamp=None):
        """ Store the graph in a string and return it.
        @param graph: the graph to be stored.
        @param language: The language code inserted into the kaf file
        @param version: The version of corefgraph set on kaf
        @param encoding: Encoding set on kaf document
        @param time_stamp: The date of coref processing set on kaf document
        @param linguistic_parsers: The linguistic parser added to kaf header.
        """
        if time_stamp is None:
            time_stamp = time.strftime(self.time_format)
        graph_builder = graph.graph["graph_builder"]

        # Check if graph contains a pre generated kaf
        try:
            previous_kaf = graph.graph["kaf"]
        except KeyError:
            previous_kaf = None

        if previous_kaf:
            kaf_document = previous_kaf
            for lp_name, lp_version, lp_layer in linguistic_parsers:
                kaf_document.add_linguistic_processors(layer=lp_layer, name=lp_name, version=lp_version,
                                                       time_stamp=time_stamp)
            for coref_index, entity in enumerate(graph_builder.get_all_entities(graph), 1):
                references = [
                    ([word["id"].split("#")[0] for word in graph_builder.get_words(mention)], mention["form"])
                    for mention in graph_builder.get_all_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)

        else:
            kaf_document = Kaf(language=language, version=version)

            words_graphs = graph_builder.get_word_graph(graph)
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

            for coref_index, entity in enumerate(graph_builder.get_all_entities(graph), 1):
                references = [([terms_ids[word] 
                                for word in graph_builder.get_words(mention)], mention["form"])
                              for mention in graph_builder.get_all_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)

        kaf_document.write(self.file, encoding=encoding)
        return kaf_document
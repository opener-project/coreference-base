from graph.graph_builder import BaseGraphBuilder
from graph.utils import GraphWrapper
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

        previous_kaf = None
        try:
            previous_kaf = GraphWrapper.get_graph_property(graph=graph, property_name="kaf")
        except:
            pass

        if previous_kaf:
            kaf_document = previous_kaf
            kaf_id = GraphWrapper.node_property(name="kaf_id", graph=graph)
            form = GraphWrapper.node_property(name='form', graph=graph)
            for lp_name, lp_version, lp_layer in linguistic_parsers:
                kaf_document.add_linguistic_processors(layer=lp_layer, name=lp_name, version=lp_version, time_stamp=time_stamp)
            for coref_index, entity in enumerate(BaseGraphBuilder.extract_entities(graph), 1):
                references = [([kaf_id[word].split("#")[0] for word in BaseGraphBuilder.get_constituent_words(mention)], form[mention])
                              for mention in BaseGraphBuilder.get_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)

        else:
            kaf_document = Kaf(language=language, version=version)

            words_graphs = BaseGraphBuilder.get_word_graph(graph)
            form = GraphWrapper.node_property(name='form', graph=graph)
            pos = GraphWrapper.node_property(name='pos', graph=graph)
            lemma = GraphWrapper.node_property(name='lemma', graph=graph)

            for lp_name, lp_version, lp_layer in linguistic_parsers:
                kaf_document.add_linguistic_processors(layer=lp_layer, name=lp_name, version=lp_version,
                                                       time_stamp=time_stamp)

            word_index = 1
            terms_ids = dict()

            for (term_index, graph_word) in enumerate(words_graphs.vertices(), 1):
                kaf_words = form[graph_word].split(" ")
                words_ids = []
                for word in kaf_words:
                    word_id = "w{0}".format(word_index)
                    kaf_document.add_word(word, word_id, lemma=lemma)
                    words_ids.append(word_id)
                    word_index += 1
                term_id = "t{0}".format(term_index)
                terms_ids[graph_word] = term_id
                kaf_document.add_term(tid=term_id, pos=pos[graph_word], words=words_ids)

            for coref_index, entity in enumerate(BaseGraphBuilder.extract_entities(graph), 1):
                references = [([terms_ids[word] for word in BaseGraphBuilder.get_constituent_words(mention)], form[mention])
                              for mention in BaseGraphBuilder.get_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)

        kaf_document.write(self.file, encoding=encoding)
        return kaf_document

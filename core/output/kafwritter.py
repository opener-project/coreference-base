from graph.graph_builder import BaseGraphBuilder
from output.basewriter import BaseDocument
from pykaf.kaf import KafDocument as Kaf
import time

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class KafDocument(BaseDocument):
    """ Store the document in a KAF format(2.1).
    """
    def store(self, graph, encoding, language=None, version=None, linguistic_parsers=(),
              time_stamp= time.strftime("%y-%m-%dT%H:%M:%S")):
        """ Store the graph in a string and return it.
        :param graph: the graph to be stored.
        :param language: The language code inserted into the kaf file
        """

        kaf_document = Kaf(language=language, version=version)

        try:
            if graph.graph_property["kafhead"][graph]:
                kaf_document.set_header(graph.graph_property["kafhead"][graph])

        except:
            pass

        words_graphs = BaseGraphBuilder.get_word_graph(graph)
        word_id = graph.vertex_properties['id']
        form = graph.vertex_properties['form']
        label = graph.vertex_properties['label']
        pos = graph.vertex_properties['pos']
        ner = graph.vertex_properties['ner']
        lemma = graph.vertex_properties['lemma']

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
                kaf_document.add_word(word, word_id)
                words_ids.append(word_id)
                word_index += 1
            term_id = "t{0}".format(term_index)
            terms_ids[graph_word] = term_id
            kaf_document.add_term(tid=term_id, pos=pos[graph_word], words=words_ids)

        for coref_index, entity in enumerate(BaseGraphBuilder.extract_entities(graph), 1):
            references = [([terms_ids[word] for word in BaseGraphBuilder.get_chunk_words(mention)], form[mention])
                          for mention in BaseGraphBuilder.get_entity_mentions(entity)]
            kaf_document.add_coreference("co{0}".format(coref_index, 1), references)
        kaf_document.write(self.file, encoding=encoding)
        return kaf_document
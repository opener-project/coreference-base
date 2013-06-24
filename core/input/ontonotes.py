__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '12/11/12'

import on


class OntoNotesReader:
    document_layer = "document"

    def __init__(self, config_file):
        self.config = on.common.util.load_config(config_file)
        self.corpus = on.ontonotes(self.config)

    def get_corpus_documents(self, subcorpus):
        return subcorpus[self.document_layer]

    def is_document(self, document):
        return document.__class__ is  on.corpora.document

    def get_document_syntax(self, sentence_id):
        return  self.corpus.subcorpus_id_list.index(sentence_id)




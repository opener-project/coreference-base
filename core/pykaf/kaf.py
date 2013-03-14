from __future__ import unicode_literals

# CONSTANT TEXT VALUES USED TO CONSTRUCT KAF
KAF_TAG = "KAF"
LANGUAGE_ATTRIBUTE = "{xml}lang"
VERSION_ATTRIBUTE = "version"
NS = {}

KAF_HEADER_TAG = "kafHeader"
NAME_ATTRIBUTE = "name"
LINGUISTIC_PROCESSOR_HEAD = "linguisticProcessors"
LAYER_ATTRIBUTE = "layer"
LINGUISTIC_PROCESSOR_OCCURRENCE_TAG = "lp"
TIMESTAMP_ATTRIBUTE = "timestamp"

SPAN_TAG = "span"
TARGET_ID_ATTRIBUTE = "id"
TARGET_TAG = "target"

TEXT_LAYER_TAG = "text"
WORD_OCCURRENCE_TAG = "wf"
WORD_ID_ATTRIBUTE = "wid"

TERMS_LAYER_TAG = "terms"
TERM_OCCURRENCE_TAG = "term"
TERM_ID_ATTRIBUTE = "tid"
NER_ATTRIBUTE = "ner"
TYPE_ATTRIBUTE = "type"
LEMMA_ATTRIBUTE = "lemma"
POS_ATTRIBUTE = "pos"

NAMED_ENTITIES_LAYER_TAG = "entities"
NAMED_ENTITY_OCCURRENCE_TAG = "entity"
NAMED_ENTITY_ID_ATTRIBUTE = "eid"
NAMED_ENTITY_TYPE_ATTRIBUTE = "type"
NAMED_ENTITY_REFERENCES_GROUP_TAG = "references"

CHUNKS_LAYER_TAG = "chunks"
CHUNK_OCCURRENCE_TAG = "chunk"
CHUNK_CASE_ATTRIBUTE = "case"
CHUNK_PHRASE_ATTRIBUTE = "phrase"
CHUNK_HEAD_ATTRIBUTE = "head"
CHUNK_ID_ATTRIBUTE = "cid"

DEPENDENCY_LAYER_TAG = "deps"
DEPENDENCY_OCCURRENCE_TAG = "dep"
DEPENDENCY_FROM_ATTRIBUTE = "from"
DEPENDENCY_FUNCTION_ATTRIBUTE = "rfunc"
DEPENDENCY_TO_ATTRIBUTE = "to"

EXTERNAL_REFERENCE_OCCURRENCE_TAG = "externalRef"
EXTERNAL_REFERENCES_TAG = "externalReferences"

COREFERENCE_LAYER_TAG = "coreferences"
COREFERENCE_ID_ATTRIBUTE = "coid"
COREFERENCE_OCCURRENCE_TAG = "coref"


__author__ = 'Josu Bermudez'

from lxml import etree


class KafDocument:
    """ Manage a KAF document.
    """
    valid_word_attributes = ("sent", "para", "offset", "length", "page")
    valid_external_attributes = ("resource", "reference", "reftype", "status", "source", "confidence")
    valid_externalRef_attributes = ("resource", "reference")

    def __init__(self, file_name=None, kaf_stream=None, language=None, version=None, kaf_header=None):
        """ Prepare the document basic structure.
        """
        if file_name:
            self.tree = etree.parse(file_name)
            self.root = self.tree.getroot()
        elif kaf_stream:
            self.root = etree.fromstring(kaf_stream)
            self.tree = etree.ElementTree(self.root)
        else:
            self.root = etree.Element(KAF_TAG, NS)
            self.tree = etree.ElementTree(self.root)
        if language:
            self.root.attrib[LANGUAGE_ATTRIBUTE] = language

        if version:
            self.root.set(VERSION_ATTRIBUTE, version)

        if not self.tree.find(KAF_HEADER_TAG):
            self.kaf_header = None
        else:
            self.kaf_header = self.tree.find(KAF_HEADER_TAG)

        if kaf_header:
            self.set_header(kaf_header)

        if not self.tree.find(TEXT_LAYER_TAG):
            self.text = etree.SubElement(self.root, TEXT_LAYER_TAG)
        else:
            self.text = self.tree.find(TEXT_LAYER_TAG)

        if not self.tree.find(TERMS_LAYER_TAG):
            self.terms = None
        else:
            self.terms = self.tree.find(TERMS_LAYER_TAG)

        if not self.tree.find(DEPENDENCY_LAYER_TAG):
            self.dependencies = None
        else:
            self.dependencies = self.tree.find(DEPENDENCY_LAYER_TAG)

        if not self.tree.find(CHUNKS_LAYER_TAG):
            self.chunks = None
        else:
            self.chunks = self.tree.find(CHUNKS_LAYER_TAG)

        if not self.tree.find(NAMED_ENTITIES_LAYER_TAG):
            self.entities = None
        else:
            self.entities = self.tree.find(NAMED_ENTITIES_LAYER_TAG)

        if not self.tree.find(COREFERENCE_LAYER_TAG):
            self.coreferences = None
        else:
            self.coreferences = self.tree.find(COREFERENCE_LAYER_TAG)

    def clear_header(self):
        self.root.remove(self.kaf_header)
        self.kaf_header = None

    def set_header(self, kaf_header):
        if self.kaf_header:
            for element in kaf_header:
                self.kaf_header.append(element)
            self.kaf_header.attrib.update(kaf_header.attrib)
        else:
            self.kaf_header = kaf_header
            self.root.append(self.kaf_header)

    def add_linguistic_processors(self, layer, name, version, time_stamp):
        if not self.kaf_header:
            self.kaf_header = etree.SubElement(self.root, KAF_HEADER_TAG)

        layer_find = self.kaf_header.find("{0}[@{1}='{2}']".format(LINGUISTIC_PROCESSOR_HEAD, LAYER_ATTRIBUTE, layer))
        if layer_find:
            layer = layer_find[0]
        else:
            layer = etree.SubElement(self.kaf_header, LINGUISTIC_PROCESSOR_HEAD, {LAYER_ATTRIBUTE: layer})

        etree.SubElement(layer, LINGUISTIC_PROCESSOR_OCCURRENCE_TAG,
                         {NAME_ATTRIBUTE: name, VERSION_ATTRIBUTE: version, TIMESTAMP_ATTRIBUTE: time_stamp})

    def add_word(self, word, wid, **kwargs):
        """Add a word to the KAF file.
        A word have the next parameters/attributes;
            + wid: the unique id for the word form.
            + sent: sentence id of the token (optional)
            + para: paragraph id (optional)
            + offset: the offset of the word form (optional)
            + length: the length of the original word form (optional)
            + page: page id (optional)
        """
        # Prepare the word attributes
        word_attributes = dict((k, v) for (k, v) in kwargs.iteritems() if k in self.valid_word_attributes)
        word_attributes[WORD_ID_ATTRIBUTE] = wid
        # Create a text subnode for the word and set its attributes
        element = etree.SubElement(self.text, WORD_OCCURRENCE_TAG, word_attributes)
        element.text = word
        return element

    def get_words(self):
        """ Return all the words in the document"""
        return self.text[:]

    def get_words_by_id(self, wid):
        """ Return all the words in the document"""
        results = self.text.find("{0}[@{1}='{2}']".format(WORD_OCCURRENCE_TAG, WORD_ID_ATTRIBUTE, wid))
        return results and results[0]

    def add_term(self, tid, pos=None, lemma=None, term_type=None, words=(), ner=None, external_refs=()):
        """Add a term to the kaf file.
        A Term have the next parameters/attributes:
            tid: unique identifier
            type: type of the term. Currently, 3 values are possible:
                + open: open category term
                + close: close category term
                + entity: term is a named entity
            lemma: lemma of the term
            pos: part of speech
            word: a list of id of the bounded words.
            external_ref: A list of dictionaries that contains the external references.
                Each reference have:
                    + resource
                    + reference
                    + INCOMPLETE
        """
        if self.terms is None:
            self.terms = etree.SubElement(self.root, TERMS_LAYER_TAG)

        #TODO Complete external references

        word_attributes = {TERM_ID_ATTRIBUTE: tid}
        if pos:
            word_attributes[POS_ATTRIBUTE] = pos
        if lemma:
            word_attributes[LEMMA_ATTRIBUTE] = lemma
        if term_type:
            word_attributes[TYPE_ATTRIBUTE] = term_type
        if ner:
            word_attributes[NER_ATTRIBUTE] = ner
        term = etree.SubElement(self.terms, TERM_OCCURRENCE_TAG, word_attributes)
        if words:
            span = etree.SubElement(term, SPAN_TAG)
            for word in words:

                etree.SubElement(span, TARGET_TAG, {TARGET_ID_ATTRIBUTE: word})
        if external_refs:
            span = etree.SubElement(term, EXTERNAL_REFERENCES_TAG)
            for external_ref in external_refs:
                ref_attributes = dict((k, v) for (k, v) in external_ref.iteritems()
                    if k in self.valid_externalRef_attributes)
                keys = ref_attributes.keys()
                for attribute in self.valid_externalRef_attributes:
                    if not attribute in keys:
                        raise Exception("External resource not have {0}".format(attribute))
                etree.SubElement(span, EXTERNAL_REFERENCE_OCCURRENCE_TAG, ref_attributes)
        return term

    def get_terms(self):
        """ Return all the words in the document"""
        return self.root.findall("{0}/{1}".format(TERMS_LAYER_TAG, TERM_OCCURRENCE_TAG))

    def get_terms_words(self, term):
        return term.findall("{0}/{1}".format(SPAN_TAG, TARGET_TAG))

    def get_terms_references(self, term):
        return term.findall("{0}/{1}".format(EXTERNAL_REFERENCES_TAG, EXTERNAL_REFERENCE_OCCURRENCE_TAG))

    def add_dependency(self, origen, to, rfunc):
        """Add a new dependency relation in the text.
        The dependency have the next parameters/attributes:
            + from: term id of the source element
            + to: term id of the target element
            + rfunc: relational function. One of:
                - mod: indicates the word introducing the dependent in a head- modifier relation.
                - subj: indicates the subject in the grammatical relation Subject-Predicate.
                - csubj, xsubj, ncsubj: The Grammatical Relations (RL)  csubj and xsubj may be used for clausal
                    subjects, controlled from within, or without,  respectively. ncsubj is a non-clausal subject.
                - dobj: Indicates the object in the grammatical relation between a predicate and its direct object.
                - iobj: The relation between a predicate and a non-clausal complement introduced by a preposition;
                    type indicates the preposition introducing the dependent.
                - obj2: The relation between a predicate and the second non-clausal complement in ditransitive
                    constructions.
        """
        if not self.dependencies:
            self.dependencies = etree.SubElement(self.root, DEPENDENCY_LAYER_TAG)


        dependency_attributes = {DEPENDENCY_FROM_ATTRIBUTE: origen,
                                 DEPENDENCY_TO_ATTRIBUTE: to,
                                 DEPENDENCY_FUNCTION_ATTRIBUTE: rfunc}
        return etree.SubElement(self.dependencies, DEPENDENCY_OCCURRENCE_TAG, dependency_attributes)

    def get_dependencies(self):
        """Return all the words in the document"""
        return self.root.findall("{0}/{1}".format(DEPENDENCY_LAYER_TAG, DEPENDENCY_OCCURRENCE_TAG))

    def add_chunk(self, cid, head, phrase, case=None, terms=()):
        """"Add a chunk to the kaf document.
        Chunks are noun or prepositional phrases, spanning terms.A chunk have the following parameters/attributes:
            + cid: unique identifier
            + head: the chunk head's term id
            + phrase: typo of the phrase.Valid values for the phrase elements are one of the following:
                - NP: noun phrase
                - VP: verbal phrase
                - PP: prepositional phrase
                - S: sentence
                - O: other
            + case (optional): declension case
        """
        # Secure the root
        if not self.chunks:
            self.chunks = etree.SubElement(self.root, CHUNKS_LAYER_TAG)
            # Prepare the attributes
        chunk_attributes = {CHUNK_ID_ATTRIBUTE: cid, CHUNK_HEAD_ATTRIBUTE: head, CHUNK_PHRASE_ATTRIBUTE: phrase}
        if case:
            chunk_attributes[CHUNK_CASE_ATTRIBUTE] = case
            # Create , and attach, the chunk
        chunk = etree.SubElement(self.chunks, CHUNK_OCCURRENCE_TAG, chunk_attributes)
        # Add the span terms
        if terms:
            spans = etree.SubElement(chunk, SPAN_TAG)
            for term in terms:
                etree.SubElement(spans, TARGET_TAG, {TARGET_ID_ATTRIBUTE: term})
        return chunk

    def get_chunks(self):
        """Return all the chunks of the text"""
        return self.root.findall("{0}/{1}".format(DEPENDENCY_LAYER_TAG, DEPENDENCY_OCCURRENCE_TAG))

    def get_chunk_terms(self, chunk):
        """Return all the terms of a chunk."""
        return chunk.findall("{0}/{1}".format(SPAN_TAG, TARGET_TAG))

    def add_entity(self, tid, entity_type, references=()):
        """ Add a entity in the document.
        :param tid: The identification code of the entity.
        :param references: The references contained in the entity.
        :param entity_type: The type of the entity.
        """

        if  self.entities is None:
            self.entities = etree.SubElement(self.root, NAMED_ENTITIES_LAYER_TAG)

        entity_attributes = {NAMED_ENTITY_ID_ATTRIBUTE: tid}
        if entity_type:
            entity_attributes[NAMED_ENTITY_TYPE_ATTRIBUTE] = entity_type
        entity = etree.SubElement(self.entities, NAMED_ENTITY_OCCURRENCE_TAG, entity_attributes)

        if references:
            for reference in references:
                span = etree.SubElement(entity, SPAN_TAG)
                for token in reference:
                    etree.SubElement(span, TARGET_TAG, {TARGET_ID_ATTRIBUTE: token})
        return entity

    def get_entities(self):
        """Return all the Named Entities in the document"""
        return self.root.findall("{0}/{1}".format(NAMED_ENTITIES_LAYER_TAG, NAMED_ENTITY_OCCURRENCE_TAG))

    def get_entity_references(self, named_entity):
        """Return all the terms of a  Named Entities in the document"""
        return named_entity.findall("{0}/{1}".format(NAMED_ENTITY_REFERENCES_GROUP_TAG, SPAN_TAG))

    def get_entity_reference_span(self, reference):
        """Return all the terms of a  Named Entities in the document"""
        return reference.findall(TARGET_TAG)

    def add_coreference(self, coid, references=()):
        """ Add a coreference cluster to the document.
        :param coid: The identification code of the cluster.
        :param references: The references contained in the cluster
        """
        if  self.coreferences is None:
            self.coreferences = etree.SubElement(self.root,COREFERENCE_LAYER_TAG)

        coref_attrib = {COREFERENCE_ID_ATTRIBUTE: coid}
        entity = etree.SubElement(self.coreferences, COREFERENCE_OCCURRENCE_TAG, coref_attrib)

        if references:
            for reference, form in references:
                entity.append(etree.Comment(form))
                span = etree.SubElement(entity, SPAN_TAG)
                for token in reference:
                    etree.SubElement(span, TARGET_TAG, {TARGET_ID_ATTRIBUTE: token})
        return entity

    def write(self, output, encoding):
        """Write document into a file.
        :param output: The output target for the document. May be a file tipe object or a file name."""
        #self.indent(self.root)
        output.write(etree.tostring(self.root, encoding=encoding, pretty_print=True, xml_declaration=True))

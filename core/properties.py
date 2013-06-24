# coding=utf-8

""" General properties

Tagset values for each language as specified in resources/tagset. Currently, we use POS, Syntactic Constituents
and NER types tagsets. The nomenclature for the files in resources/target is used to instantiate the variables
below. For example, pos_tag_set will expect a file end in '_pos', such as 'tagset_pos'. The same applies to
'_constituent' and '_ner'.

"""
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

lang = None

pos_tag_set = None
constituent_tag_set = None
ner_tag_set = None


def set_lang(lang_code):
    """ set the module properties from  a specific language properties

    """
    lang_properties = __import__("properties_{0}".format(lang_code), globals=globals(), locals=locals())
    global lang
    global pos_tag_set
    global constituent_tag_set
    global ner_tag_set
    lang = lang_properties.lang
    pos_tag_set = lang_properties.pos_tag_set
    constituent_tag_set = lang_properties.constituent_tag_set
    ner_tag_set = lang_properties.ner_tag_set




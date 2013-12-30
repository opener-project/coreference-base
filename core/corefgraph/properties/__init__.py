# coding=utf-8
""" General properties

Tagset values for each language as specified in resources/tagset. Currently, we use POS, Syntactic Constituents
and NER types tagsets. The nomenclature for the files in resources/target is used to instantiate the variables
below. For example, pos_tag_set will expect a file end in '_pos', such as 'tagset_pos'. The same applies to
'_constituent' and '_ner'.

"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '10/30/13'

import logging
import logging.config
import os
import sys

default_ner_tag_set = "default"
default_dep_tag_set = "default"


try:
    import yaml
    try:
        config_filename = os.path.abspath(os.path.join(__path__[0], 'logging.conf'))
        logging.config.dictConfig(yaml.load(open(config_filename)))
    except Exception as ex:
        import sys
        print "NO LOGGING: {0} \nfails: {1}".format(config_filename, ex)
except Exception as ex:
    sys.stdout.write("Error importing yalm: " + str(ex))


lang = None

pos_tag_set = None
constituent_tag_set = None
ner_tag_set = None

module_path = os.path.join(os.path.split(__path__[0])[0], "resources")


def set_lang(lang_code):
    """ set the module properties from  a specific language properties

    """
    lang_properties = __import__("properties_{0}".format(lang_code), globals=globals(), locals=locals())
    global lang
    global pos_tag_set
    global constituent_tag_set
    global ner_tag_set
    global dep_tag_set
    lang = lang_properties.lang
    pos_tag_set = lang_properties.pos_tag_set
    constituent_tag_set = lang_properties.constituent_tag_set
    try:
        ner_tag_set = lang_properties.ner_tag_set
    except:
        ner_tag_set = default_ner_tag_set
    try:
        dep_tag_set = lang_properties.dep_tag_set
    except:
        dep_tag_set = default_dep_tag_set

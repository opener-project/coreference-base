# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from . import logger
from ..features import utils
from ..resources.dictionaries import pronouns
from .. import properties
from ..resources.tagset import pos_tags, ner_tags

import os


# The o comes from IOB tagging not from first letter of org
singular_ne = lambda x: ner_tags.all(x) and not ner_tags.organization(x)
# norp?
singular_pronouns = pronouns.singular
plural_pronouns = pronouns.plural

plural_words = utils.load_file(
    os.path.join(properties.module_path, "files/number/{0}.plural.unigrams.txt".format(properties.lang)))
singular_words = utils.load_file(
    os.path.join(properties.module_path, "files/number/{0}.singular.unigrams.txt".format(properties.lang)))


# based on the eagle tag set
try:
    plural_pos = pos_tags.plural
except:
    plural_pos = lambda x: False
    logger.warning("Dummy number(PLURAL) POS checker\n")

try:
    singular_pos = pos_tags.singular
except:
    singular_pos = lambda x: False
    logger.warning("Dummy animacy POS(SINGULAR) checker\n")
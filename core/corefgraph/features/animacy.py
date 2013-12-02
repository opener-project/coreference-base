# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from . import logger
from ..features import utils
from ..resources.dictionaries import pronouns
from ..resources.tagset import ner_tags
from ..resources.tagset import pos_tags
from .. import properties

import os


animate_pronouns = pronouns.animate
inanimate_pronouns = pronouns.inanimate

animate_words = utils.load_file(
    os.path.join(properties.module_path, "files/animate/{0}.animate.unigrams.txt".format(properties.lang)))
inanimate_words = utils.load_file(
    os.path.join(
        properties.module_path, "files/animate/{0}.inanimate.unigrams.txt".format(properties.lang)))

animate_ne = ner_tags.animate
inanimate_ne = ner_tags.inanimate


try:
    animate_pos = pos_tags.animate
except Exception as ex:
    animate_pos = lambda x: False
    logger.warning("Dummy animacy POS checker\n")

try:
    inanimate_pos = pos_tags.inanimate
except Exception as ex:
    inanimate_pos = lambda x: False
    logger.warning("Dummy animacy(IN) POS checker\n")
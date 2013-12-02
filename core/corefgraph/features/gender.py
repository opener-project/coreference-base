# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from . import logger
from ..features import utils
from ..resources.dictionaries import pronouns
from ..resources.tagset import pos_tags
from .. import properties

import os


female_pronouns = pronouns.female
male_pronouns = pronouns.male
neutral_pronouns = pronouns.neutral

neutral_words = utils.load_file(
    os.path.join(properties.module_path, "files/gender/{0}.neutral.unigrams.txt".format(properties.lang)))
male_words = utils.load_file(
    os.path.join(properties.module_path, "files/gender/{0}.male.unigrams.txt".format(properties.lang)))
female_words = utils.load_file(
    os.path.join(properties.module_path, "files/gender/{0}.female.unigrams.txt".format(properties.lang)))
female_names, male_names = utils.split_gendername_file(
    os.path.join(properties.module_path, "files/gender/{0}.namegender.combine.txt".format(
        properties.lang)))


bergma_counter = None


def get_bergma_dict():
    global bergma_counter
    if bergma_counter is None:
        bergma_counter = utils.bergma_split(
            os.path.join(properties.module_path, "files/gender/{0}.gender.data".format(properties.lang)))
        logger.debug("Bergma dict: %i", len(bergma_counter))
    return bergma_counter

try:
    male_pos = pos_tags.male
except Exception as ex:
    male_pos = lambda x: False
    logger.warning("Dummy gender(MALE) POS checker\n")

try:
    female_pos = pos_tags.female
except:
    female_pos = lambda x: False
    logger.warning("Dummy gender(FEMALE) POS checker\n")

try:
    neutral_pos = pos_tags.neutral
except:
    neutral_pos = lambda x: False
    logger.warning("Dummy gender(NEUTRAL) POS checker\n")

from features import utils
from resources.dictionaries import pronouns
import properties

from resources.tagset import pos_tags
import sys

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

female_pronouns = pronouns.female
male_pronouns = pronouns.male
neutral_pronouns = pronouns.neutral

neutral_words = utils.load_file("resources/files/gender/{0}.neutral.unigrams.txt".format(properties.lang))
male_words = utils.load_file("resources/files/gender/{0}.male.unigrams.txt".format(properties.lang))
female_words = utils.load_file("resources/files/gender/{0}.female.unigrams.txt".format(properties.lang))

female_names, male_names = utils.split_gendername_file("resources/files/gender/{0}.namegender.combine.txt".format(
    properties.lang))

counter = utils.bergma_split("resources/files/gender/{0}.gender.data".format(properties.lang))

try:
    male_pos = pos_tags.male
except:
    male_pos = lambda x: False
    sys.stderr.write("Dummy gender(MALE) POS checker\n")

try:
    female_pos = pos_tags.female
except:
    female_pos = lambda x: False
    sys.stderr.write("Dummy gender(FEMALE) POS checker\n")

try:
    neutral_pos = pos_tags.neutral
except:
    neutral_pos = lambda x: False
    sys.stderr.write("Dummy animacy(NEUTRAL) POS checker\n")

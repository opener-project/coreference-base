from features import utils
from resources.dictionaries import pronouns
import properties


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
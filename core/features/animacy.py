from features import utils
from resources.dictionaries import pronouns
from resources.tagset import ner_tags
import properties

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

animate_pronouns = pronouns.animate

inanimate_pronouns = pronouns.inanimate

animate_words = utils.load_file("resources/files/animate/{0}.animate.unigrams.txt".format(properties.lang))
inanimate_words = utils.load_file("resources/files/animate/{0}.inanimate.unigrams.txt".format(properties.lang))

animate_ne = ner_tags.animate

inanimate_ne = ner_tags.inanimate


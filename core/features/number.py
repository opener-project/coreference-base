from features import utils
from resources.dictionaries import pronouns
from resources.tagset import english_types_ner
import properties


__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


# The o comes from IOB tagging not from first letter of org
single_ne = english_types_ner.single_ner
# norp?
singular_pronouns = pronouns.singular
plural_pronouns = pronouns.plural

plural_words = utils.load_file("resources/files/number/{0}.plural.unigrams.txt".format(properties.lang))
singular_words = utils.load_file("resources/files/number/{0}.singular.unigrams.txt".format(properties.lang))

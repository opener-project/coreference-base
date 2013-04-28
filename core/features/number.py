from features import utils
from resources.dictionaries import pronouns
import properties


__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


# The o comes from IOB tagging not from first letter of org
unknown_ne_tag = ("o", "org", "organization")
# norp?
singular_pronouns = pronouns.singular
plural_pronouns = pronouns.plural

plural_words = utils.load_file("resources/files/number/{0}.plural.unigrams.txt".format(properties.lang))
singular_words = utils.load_file("resources/files/number/{0}.singular.unigrams.txt".format(properties.lang))

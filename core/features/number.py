from features import utils
from resources.dictionaries import pronouns
import properties
from resources.tagset import pos_tags, ner_tags
import sys

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


# The o comes from IOB tagging not from first letter of org
singular_ne =  lambda x: ner_tags.all(x) and not ner_tags.organization(x)
# norp?
singular_pronouns = pronouns.singular
plural_pronouns = pronouns.plural

plural_words = utils.load_file("resources/files/number/{0}.plural.unigrams.txt".format(properties.lang))
singular_words = utils.load_file("resources/files/number/{0}.singular.unigrams.txt".format(properties.lang))


# based on the eagle tag set
try:
    plural_pos = pos_tags.plural
except:
    plural_pos = lambda x: False
    sys.stderr.write("Dummy number(PLURAL) POS checker\n")

try:
    singular_pos = pos_tags.singular
except:
    singular_pos = lambda x: False
    sys.stderr.write("Dummy animacy POS(SINGULAR) checker\n")
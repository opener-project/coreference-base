from features import utils
from resources.dictionaries import pronouns
from resources.tagset import ner_tags
import properties
import sys

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

animate_pronouns = pronouns.animate
inanimate_pronouns = pronouns.inanimate

animate_words = utils.load_file("resources/files/animate/{0}.animate.unigrams.txt".format(properties.lang))
inanimate_words = utils.load_file("resources/files/animate/{0}.inanimate.unigrams.txt".format(properties.lang))

animate_ne = ner_tags.animate
inanimate_ne = ner_tags.inanimate


from resources.tagset import pos_tags
try:
    animate_pos = pos_tags.animate
except:
    animate_pos = lambda x: False
    sys.stderr.write("Dummy animacy POS checker\n")

try:
    inanimate_pos = pos_tags.inanimate
except:
    inanimate_pos = lambda x: False
    sys.stderr.write("Dummy animacy(IN) POS checker\n")

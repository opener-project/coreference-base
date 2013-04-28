from features import utils
from resources.dictionaries import pronouns
import properties

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

animate_pronouns = pronouns.animate

inanimate_pronouns = pronouns.inanimate

animate_words = utils.load_file("resources/files/animate/{0}.animate.unigrams.txt".format(properties.lang))
inanimate_words = utils.load_file("resources/files/animate/{0}.inanimate.unigrams.txt".format(properties.lang))

animate_ne = ("person",
              "per")

inanimate_ne = ('facility',
                'norp',
                'location','loc',
                'product',
                'event',
                'organization','org'
                'work of art',
                'law',
                'language',
                'date',
                'time',
                'percent',
                'money',
                'number',
                'quantity',
                'ordinal',
                'cardinal',
                'misc',
                'veh',
                'fac',
                'gpe',
                'wea',
                )
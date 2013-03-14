from resources import utils
import pronouns
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

female_pronouns = pronouns.female
male_pronouns = pronouns.male
neutral_pronouns = pronouns.neutral

neutral_words = utils.load_file("resources/files/gender/neutral.unigrams.txt")
male_words = utils.load_file("resources/files/gender/male.unigrams.txt")
female_words = utils.load_file("resources/files/gender/female.unigrams.txt")

female_names, male_names =  utils.split_gendername_file("resources/files/gender/namegender.combine.txt")

counter = utils.bergma_split("resources/files/gender/gender.data")
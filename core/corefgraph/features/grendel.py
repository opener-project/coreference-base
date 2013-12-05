# coding=utf-8
""" Gender and number extractor form a text mention """

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from . import logger
from ..features.gender import female_pronouns, male_pronouns, neutral_pronouns, female_words, male_words,\
    neutral_words, female_names, male_names, get_bergma_dict, male_pos, female_pos, neutral_pos
from ..features.number import plural_pronouns, plural_words, singular_pronouns, singular_words, singular_ne, \
    singular_pos, plural_pos
from ..features.animacy import animate_words, inanimate_words, inanimate_pronouns, animate_pronouns,\
    animate_ne, inanimate_ne, animate_pos, inanimate_pos
from ..resources.dictionaries import pronouns
from ..resources.tagset import pos_tags, ner_tags

import re


class GenderNumberExtractor():
    """ Gender selector based on the work in Stanford Coreference System http://nlp.stanford.edu/software/dcoref.html
    """
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"
    SINGULAR = "singular"
    PLURAL = "plural"
    ANIMATE = "animate"
    INANIMATE = "inanimate"
    use_bergsma_gender_lists = True
    use_bergsma_number_lists = True
    use_names_list = True
    use_probabilistic_gender_classification = "probabilistic_gender"

    prominence_boost = 0.5
    threshold = 2

    all_pronouns = female_pronouns, male_pronouns, neutral_pronouns

    def __init__(self, probabilistic_gender=False):
        self.counter = None
        self.probabilistic_gender_classification = probabilistic_gender

    def count(self, form):
        """ Count the male, female, neutral and plural occurrences in Bersmas(Bergmas an lin) list.
        @param form: The form of the word
        """
        if self.counter is None:
            self. counter = get_bergma_dict()
        male, female, neutral, plural = self.counter.get(form, (0, 0, 0, 0))
        return int(male), int(female), int(neutral), int(plural)

    def get_gender(self, word_form, word_pos):
        """Determines the gender of the word.
        @param word_form: The form of the word
        @param word_pos: The POS of the word
        """
        # If if a pronoun search in the pronouns list for a mach
        word_form = word_form.lower()
        word_pos = word_pos
        # Use the mention POS to determine the feature
        if male_pos(word_pos):
            return self.MALE
        if female_pos(word_pos):
            return self.FEMALE
        if neutral_pos(word_pos):
            return self.NEUTRAL
        # Pronoun search
        if word_pos == pos_tags.pronouns or word_form in pronouns.all:
            logger.debug("Is a pronoun")
            if word_form in male_pronouns:
                return self.MALE
            if word_form in female_pronouns:
                return self.FEMALE
            if word_form in neutral_pronouns:
                return self.NEUTRAL

        elif self.use_names_list:
            logger.debug("Using name List")
            if word_form in female_names:
                return self.FEMALE
            elif word_form in male_names:
                return self.MALE
        # WILD ZONE
        elif self.use_bergsma_gender_lists:
            logger.debug("Using Bergsma List")
            if word_form in male_words:
                return self.MALE
            if word_form in female_words:
                return self.FEMALE
            if word_form in neutral_words:
                return self.NEUTRAL
                # Bergmas 2005 list search

        elif self.probabilistic_gender_classification:
            logger.debug("Using Bergmas an lin 2006 probabilistic gender classification")
            male, female, neutral, plural = self.count(word_form)
            if (male * self.prominence_boost > female + neutral) and (male > self.threshold):
                return self.MALE
            elif (female * self.prominence_boost > male + neutral) and (female > self.threshold):
                return self.FEMALE
            elif (neutral * self.prominence_boost > male + female) and (neutral > self.threshold):
                return self.NEUTRAL

        return self.UNKNOWN

    def get_number(self, word_form, word_pos, word_ner):
        """Determines the number of the word and return a constant.
        @param word_ner: The ner of the word
        @param word_form: The form of the word
        @param word_pos: The POS of the word
        """
        # Normalize parameters
        word_ner = word_ner
        word_form = word_form.lower()
        word_pos = word_pos

        # Use the mention POS to determine the feature
        if singular_pos(word_pos):
            return self.SINGULAR
        if plural_pos(word_pos):
            return self.PLURAL
        # Pronouns
        if pos_tags.pronouns(word_pos) or word_form in pronouns.all:
            if word_form in plural_pronouns:
                return self.PLURAL
            elif word_form in singular_pronouns:
                return self.SINGULAR
                # Bergsma Lists
        if self.use_bergsma_number_lists:
            if word_form in singular_words:
                return self.SINGULAR
            if word_form in plural_words:
                return self.PLURAL
                # WILD ZONE
        # NER
        if singular_ne(word_ner):
            # Ner are singular by default except organizations
            return self.SINGULAR
        # NOUNS
        # TODO mote this to first rule
        if word_pos.startswith("n"):
            if word_pos.endswith("s"):
                return self.PLURAL
            else:
                return self.SINGULAR
        # TODO manage the AND causes
        # Mention sub tree : maneja los casos con and
#        enumerationPattern = r"NP < (NP=tmp $.. (/,|CC/ $.. NP))";
#        tgrepPattern = re.compile(enumerationPattern)
#        match= tgrepPattern.matcher(this.mentionSubTree)
#        while  m.find():
#            if(this.mentionSubTree==m.getNode("tmp") and this.spanToString().toLowerCase().contains(" and ")):
#                number = Number.PLURAL
        return self.UNKNOWN

    def get_animacy(self, word_form, word_pos, word_ner):
        """Determines the gender of the word.
        @param word_ner: The ner of the word
        @param word_form: The form of the word
        @param word_pos: The POS of the word
        """
        # Normalize parameters
        normalized_ner = word_ner.lower()
        normalized_form = word_form.lower()
        normalized_form = re.sub("\d", "0", normalized_form)
        normalized_pos = word_pos.replace("$", "")
        # Use the mention POS to determine the feature
        if inanimate_pos(word_pos):
            return self.INANIMATE
        if animate_pos(word_pos):
            return self.ANIMATE
        # Pronouns
        if pos_tags.pronouns(normalized_pos) or normalized_form in pronouns.all:
            if normalized_form in inanimate_pronouns:
                return self.INANIMATE
            elif normalized_form in animate_pronouns:
                return self.ANIMATE
            else:
                return self.UNKNOWN
                # Bergsma Lists
        elif self.use_bergsma_number_lists:
            if word_form in animate_words:
                return self.ANIMATE
            if word_form in inanimate_words:
                return self.INANIMATE
        # NER
        elif normalized_ner and normalized_ner != ner_tags.no_ner:
            if normalized_ner in animate_ne:
                return self.ANIMATE
            elif normalized_ner in inanimate_ne:
                return self.INANIMATE
        return self.UNKNOWN

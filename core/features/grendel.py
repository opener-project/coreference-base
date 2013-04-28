""" Gender and number extractor form a text mention """

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

import re
from logging import getLogger

from features.gender import female_pronouns, male_pronouns, neutral_pronouns, female_words, male_words,\
    neutral_words, female_names, male_names, counter
from features.number import plural_pronouns, plural_words, singular_pronouns, singular_words, unknown_ne_tag
from features.animacy import animate_words, inanimate_words, inanimate_pronouns, animate_pronouns,\
    animate_ne, inanimate_ne

from resources.dictionaries import pronouns
from resources.tagset import pos_tags


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
    use_probabilistic_gender_classification = True

    prominence_boost = 0.5
    threshold = 2

    all_pronouns = female_pronouns, male_pronouns, neutral_pronouns

    def __init__(self, logger=getLogger('GenderNumberExtractor')):
        self.logger = logger

    def count(self, form):
        """ Count the male, female, neutral and plural occurrences in Bersmas(Bergmas an lin) list.
        """
        male, female, neutral, plural = counter[form]
        return int(male), int(female), int(neutral), int(plural)

    def get_gender(self, form, pos):
        """Determines the gender of the referent and return a constant."""
        # If if a pronoun search in the pronouns list for a mach
        form = form.lower()
        pos = pos.lower()
        # Pronoun search
        if pos == pos_tags.pronouns or form in pronouns.all:
            self.logger.debug("Is a pronoun")
            if form in male_pronouns:
                return self.MALE
            if form in female_pronouns:
                return self.FEMALE
            if form in neutral_pronouns:
                return self.NEUTRAL
        elif self.use_probabilistic_gender_classification:
            self.logger.debug("Using Bergmas an lin 2006 probabilistic gender classification")
            male, female, neutral, plural = self.count(form)
            if (male * self.prominence_boost > female + neutral) and (male > self.threshold):
                return self.MALE
            elif (female * self.prominence_boost > male + neutral) and (female > self.threshold):
                return self.FEMALE
            elif (neutral * self.prominence_boost > male + female) and (neutral > self.threshold):
                return self.NEUTRAL
        # Bergmas 2005 list search
        elif self.use_bergsma_gender_lists:
            self.logger.debug("Using Bergsma List")
            if form in male_words:
                return self.MALE
            if form in female_words:
                return self.FEMALE
            if form in neutral_words:
                return self.NEUTRAL
        elif self.use_names_list:
            self.logger.debug("Using name List")
            if form in female_names:
                return self.FEMALE
            elif form in male_names:
                return self.MALE
            # WILD ZONE
        return self.UNKNOWN

    def get_number(self, form, pos, ner):
        # Normalize parameters
        ner = ner.lower()
        form = form.lower()
        pos = pos.lower()
        # Pronouns
        if pos in pos_tags.pronouns or form in pronouns.all:
            if form in  plural_pronouns:
                return self.PLURAL
            elif form in singular_pronouns:
                return self.SINGULAR
                # Bergsma Lists
        if self.use_bergsma_number_lists:
            if form in singular_words:
                return self.SINGULAR
            if form in plural_words:
                return self.PLURAL
                # WILD ZONE
        # NER
        if ner in unknown_ne_tag:
            # Ner are singular by default except organizations
            return self.SINGULAR
         # NOUNS
        if pos.startswith("n"):
            if pos.endswith("s"):
                return self.PLURAL
            else:
                return self.SINGULAR
        # Mention sub tree : maneja los casos con and
#        enumerationPattern = r"NP < (NP=tmp $.. (/,|CC/ $.. NP))";
#        tgrepPattern = re.compile(enumerationPattern)
#        match= tgrepPattern.matcher(this.mentionSubTree)
#        while  m.find():
#            if(this.mentionSubTree==m.getNode("tmp") and this.spanToString().toLowerCase().contains(" and ")):
#                number = Number.PLURAL
        return self.UNKNOWN

    def get_animacy(self, form, pos, ner):
        # Normalize parameters
        normalized_ner = ner.lower()
        normalized_form = form.lower()
        normalized_form = re.sub("\d", "0", normalized_form)
        normalized_pos = pos.lower().replace("$", "")
        # Pronouns
        if normalized_pos in pos_tags.pronouns or normalized_form in pronouns.all:
            if normalized_form in inanimate_pronouns:
                return self.INANIMATE
            elif normalized_form in animate_pronouns:
                return self.ANIMATE
            else:
                return self.UNKNOWN
                # Bergsma Lists
        elif self.use_bergsma_number_lists:
            if form in animate_words:
                return self.ANIMATE
            if form in inanimate_words:
                return self.INANIMATE
        # NER
        elif normalized_ner and normalized_ner != "o":
            if normalized_ner in animate_ne:
                return self.ANIMATE
            elif normalized_ner in inanimate_ne:
                return self.INANIMATE

        return self.UNKNOWN

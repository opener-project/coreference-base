from multisieve.sieves.base import Sieve
from features.grendel import GenderNumberExtractor
from resources.tagset import ner_tags

UNKNOWN = GenderNumberExtractor.UNKNOWN
NO_NER = ner_tags.no_ner
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class PronounMatch(Sieve):
    """ To mentions are coreferent if their surfaces are equals."""
    SENTENCE_DISTANCE_LIMIT = 3

    sort_name = "PM"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """ Only pronouns can be used for this sieve"""
        return mention["mention"] == "pronoun_mention"

    def are_coreferent(self, entity, mention, candidate):
        a = 3
        if self.tree_utils.sentence_distance(mention, candidate) > self.SENTENCE_DISTANCE_LIMIT:
            return False

        if ((
                UNKNOWN in self.entity_property(entity, "gender") or
                UNKNOWN in self.candidate_property(candidate, "gender") or
                self.candidate_property(candidate, "gender").intersection(self.entity_property(entity, "gender"))) and
            (
                UNKNOWN in self.entity_property(entity, "number") or
                UNKNOWN in self.candidate_property(candidate, "number") or
                self.candidate_property(candidate, "number").intersection(self.entity_property(entity, "number"))) and
            (
                UNKNOWN in self.entity_property(entity, "animacy") or
                UNKNOWN in self.candidate_property(candidate, "animacy") or
                self.candidate_property(candidate, "animacy").intersection(self.entity_property(entity, "animacy"))) and
            (
                NO_NER in self.entity_property(entity, "ner") or
                NO_NER in self.candidate_property(candidate, "ner") or
                self.candidate_property(candidate, "ner").intersection(self.entity_property(entity, "ner")))):
            return True
        return False



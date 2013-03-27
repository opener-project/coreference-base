from multisieve.sieves.base import Sieve
from multisieve.dictionaries import UNKNOWN

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class PronounMatch(Sieve):
    """ To mentions are coreferent if their surfaces are equals."""
    SENTENCE_DISTANCE_LIMIT = 3

    sort_name = "PM"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        return self.mention_type[mention] == "pronoun_mention"

    def are_coreferent(self, entity, index, candidate):
        #if self.graph_builder.sentence_distance(entity[index], candidate) > self.SENTENCE_DISTANCE_LIMIT:
        #    return False
        a = 2
        if ((
                UNKNOWN in self.entity_property(entity, "gender") or
                UNKNOWN in self.candidate_property(candidate, "gender") or
                self.candidate_property(candidate, "gender").intersection(self.entity_property(entity, "gender"))) and
            (
                UNKNOWN in self.entity_property(entity, "number") or
                UNKNOWN in self.candidate_property(candidate, "number") or
                self.candidate_property(candidate, "number").intersection(self.entity_property(entity, "number"))) and
            (
                UNKNOWN in self.entity_property(entity, "animate") or
                UNKNOWN in self.candidate_property(candidate, "animate") or
                self.candidate_property(candidate, "animate").intersection(self.entity_property(entity, "animate"))) and
            (
                "o" in self.entity_property(entity, "ner") or
                "o" in self.candidate_property(candidate, "ner") or
                self.candidate_property(candidate, "ner").intersection(self.entity_property(entity, "ner")))):
            return True
        return False



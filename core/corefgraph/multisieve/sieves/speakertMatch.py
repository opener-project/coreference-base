# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ...multisieve.sieves.base import Sieve
from ...resources.dictionaries import pronouns
from ...resources.tagset import dependency_tags


class SpeakerSieve(Sieve):
    """ Check the coreference of two mentions with rules based in speaker relations."""
    sort_name = "SM"

    ONLY_FIRST_MENTION = False
    NO_PRONOUN = False

    # Default behavior.
    configs = set(["SPEAKER_WE_WE", "SPEAKER_I_I", "SPEAKER_YOU_YOU", "SPEAKER_I", "SPEAKER_I_YOU", "SPEAKER_REFLEX"])
    WE_MATCH = False
    I_MATCH = True
    YOU_MATCH = True
    SPEAKER_I_MATCH = False
    YOU_I_MATCH = False
    SPEAKER_REFLEX = True
    DEBUG = False

    def __init__(self, multi_sieve_processor, options):
        Sieve.__init__(self, multi_sieve_processor, options)
        self.logger.debug("Options: %s", options)
        if len(self.configs.intersection(set(options))):
            # If exist any config rewrite options in other case use default
            self.WE_MATCH = "SPEAKER_WE_WE" in options
            self.I_MATCH = "SPEAKER_I_I" in options
            self.YOU_MATCH = "SPEAKER_YOU_YOU" in options
            self.SPEAKER_I_MATCH = "SPEAKER_I" in options
            self.YOU_I_MATCH = "SPEAKER_I_YOU" in options
            self.SPEAKER_REFLEX = "SPEAKER_REFLEX" in options
        else:
            self.logger.debug("SPEAKER Default options")

    def are_coreferent(self, entity, mention, candidate):
        """ Mention and candidate are the same person in a Discourse.
        """
        if not super(self.__class__, self).are_coreferent(entity, mention, candidate):
            return False
        if self.SPEAKER_REFLEX and self.reflexive(mention, candidate):
            self.logger.debug("SPEAKER_REFLEX: %s %s", mention["form"], candidate["form"])
            return True
        # "I" and the speaker
        if self.SPEAKER_I_MATCH and self.is_I(candidate) and self.is_speaker(mention):
            if self.are_speaker_speech(speaker=mention, speech=candidate):
                self.logger.debug("SPEAKER_I_MATCH: %s %s", mention["form"], candidate["form"])
                return True
            else:
                self.invalid(mention, candidate)

        if self.SPEAKER_I_MATCH and self.is_I(mention) and self.is_speaker(candidate):
            if self.are_speaker_speech(speaker=candidate, speech=mention):
                self.logger.debug("SPEAKER_I_MATCH: %s %s", mention["form"], candidate["form"])
                return True
            else:
                self.invalid(mention, candidate)

        # Two "I" in the same speaker speech
        if self.I_MATCH and self.is_I(mention) and self.is_I(candidate):
            if self.same_speaker(mention, candidate):
                self.logger.debug("SPEAKER_I_I_MATCH: %s %s", mention["form"], candidate["form"])
                return True
            else:
                self.invalid(mention, candidate)

        # Two "We" in the same speaker speech
        if self.WE_MATCH and self.is_we(mention) and self.is_we(candidate):
            if self.same_speaker(mention, candidate):
                self.logger.debug("SPEAKER_WE_WE_MATCH: %s %s", mention["form"], candidate["form"])
                return True
            else:
                self.invalid(mention, candidate)

        # Two "you" in the same speaker Speech (NOT FOUND IN CODE)
        if self.YOU_MATCH and  \
                self.is_you(mention) and self.is_you(candidate):
            if self.same_speaker(mention, candidate):
                self.logger.debug("SPEAKER_YOU_YOU_MATCH: %s %s", mention["form"], candidate["form"])
                return True
            else:
                self.invalid(mention, candidate)
        # previous I - you or previous you - I in two person conversation (NOT IN PAPER)
        if self.YOU_I_MATCH and mention["doc_type"] == "conversation" and \
                ((self.is_you(mention) and self.is_I(candidate)) or
                (self.is_I(mention) and self.is_you(candidate))):
            if not self.same_speaker(mention, candidate) and (abs(mention["utterance"] - candidate["utterance"] == 1)):
                self.logger.debug("SPEAKER_YOU_I_MATCH: %s %s", mention["form"], candidate["form"])
                return True
            else:
                self.invalid(mention, candidate)

        return False

    def reflexive(self, mention, candidate):
        """check if the mention candidate is a reflexive relation."""
        if mention["form"].lower() not in pronouns.reflexive:
            return False
        if not self.graph_builder.same_sentence(mention, candidate):
            return False
        mention_head = self.graph_builder.get_head_word(mention)
        candidate_head = self.graph_builder.get_head_word(candidate)
        mention_deps = self.graph_builder.get_governor_words(mention_head)
        candidate_deps = self.graph_builder.get_governor_words(candidate_head)
        for node, relation in mention_deps:
            if dependency_tags.subject(relation["value"]):
                for node_b, relation_b in candidate_deps:
                    if node["id"] == node_b["id"] and dependency_tags.object(relation_b["value"]):
                        return True
            if dependency_tags.object(relation["value"]):
                for node_b, relation_b in candidate_deps:
                    if node["id"] == node_b["id"] and dependency_tags.subject(relation_b["value"]):
                        return True
        return False

    def are_speaker_speech(self, speaker, speech):
        speech_speaker = speech["speaker"]
        if type(speech_speaker) is not dict:
            return False
        #TODO check this Only heads??
        speaker_words_ids = [word["id"] for word in self.graph_builder.get_words(speaker)]
        return speech_speaker["id"] in speaker_words_ids

    def is_speaker(self, mention):
        #TODO check if only head
        speaker_words = self.graph_builder.get_words(mention)
        for word in speaker_words:
            if word.get("is_speaker", False):
                return True
        return False

    def is_speech(self, mention):
        return mention.get("quoted", False)

    def invalid(self, mentionA, mentionB):
        pass

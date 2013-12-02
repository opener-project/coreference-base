# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ...multisieve.sieves.base import Sieve
from ...resources.dictionaries import stopwords
from ...resources.tagset import pos_tags


class StrictHeadMatching(Sieve):
    """ A relative pronoun is referent to the NP that modified."""
    FIRST_MENTION = True
    sort_name = "SHM"

    ONLY_FIRST_MENTION = True
    NO_PRONOUN = True
    DISCOURSE_SALIENCE = True
    NO_STOP_WORDS = True

    def get_head_word_form(self, element):
        """ Get the head of a chunk
        """
        head = self.graph_builder.get_head_word(element)
        # if head is None return None. If not return head form
        return head["form"]

    def get_modifiers(self, element):
        """ Get the chunk forms list that are related to a chunk by a mod dependency.
        """
        chunk_head = self.get_head_word_form(element)
        all_mods = set([word["form"].lower() for word in self.graph_builder.get_words(element)
                        if pos_tags.mod_forms(word["pos"])]) - set(chunk_head)
        return all_mods

    def get_all_word(self, element):
        """ Get the chunk forms list that are related to a chunk by a mod dependency.
        """
        all_mods = set([word["form"].lower() for word in self.graph_builder.get_words(element)])
        return all_mods

    def entity_head_match(self, mention, candidate_entities):
        """Checks if the head of the candidate is the head word of any mention of the entity.
        """

        for candidate_entity in candidate_entities:
            for candidate_entity_mention in candidate_entity:
                if self.get_head_word_form(candidate_entity_mention).lower() == \
                        self.get_head_word_form(mention).lower():
                    return True
        return False

    def word_inclusion(self, entity, mention, candidate_entities):
        # Change mention / candidates form
        candidate_words = set([
            word["form"].lower()
            for candidate_entity in candidate_entities
            for candidate_mention in candidate_entity
            for word in self.graph_builder.get_words(candidate_mention)])
        entity_words = set([
            word["form"].lower()
            for n_mention in entity
            for word in self.graph_builder.get_words(n_mention)])
        entity_words.remove(self.get_head_word_form(mention).lower())
        entity_words.difference_update(stopwords.extended_stop_words)
        entity_words.difference_update(stopwords.stop_words)

        return len(entity_words - candidate_words) == 0

    def compatible_modifiers_only(self, entity, candidate_entities):
        """Check if all the modifiers of the candidate appears in the first mention of the entity.
        """
        for candidate_entity in candidate_entities:
            for candidate_mention in candidate_entity:
                for entity_mention in entity:
                    candidate_words = self.get_all_word(candidate_mention)
                    mention_modifiers = self.get_modifiers(entity_mention)
                    for location_modifier in stopwords.location_modifiers:
                        if (location_modifier in candidate_words) and (location_modifier not in mention_modifiers):
                            return False
                    if len(mention_modifiers - candidate_words) > 0:
                        return False
        return True

    def are_coreferent(self, entity, mention, candidate):

        if Sieve.are_coreferent(self, entity, mention, candidate):
            return False

        if self.is_pronoun(candidate):
            return False

        candidate_entities = [[self.graph.node[candidate_mention] for candidate_mention in candidate_entity]
                              for candidate_entity in self.entities_of_a_mention(candidate)]
        entity_mentions = [self.graph.node[m] for m in entity]

        if self.i_within_i(mention_a=mention, mention_b=candidate):
            return False
        if not self.entity_head_match(mention=mention, candidate_entities=candidate_entities):
            return False
        if not self.word_inclusion(entity=entity_mentions, mention=mention, candidate_entities=candidate_entities):
            return False
        if not self.compatible_modifiers_only(entity=entity_mentions, candidate_entities=candidate_entities):
            return False
        return True


class StrictHeadMatchingVariantA(StrictHeadMatching):
    """ A variation of SHM that no check compatible modifiers. """

    sort_name = "SHMA"

    ONLY_FIRST_MENTION = True
    NO_PRONOUN = True
    DISCOURSE_SALIENCE = True
    NO_STOP_WORDS = True

    def compatible_modifiers_only(self, entity, candidate_entities):
        """ Void this filtering
        @param entity: Irrelevant
        @param candidate_entities: Irrelevant
        @return: Always True
        """

        return True


class StrictHeadMatchingVariantB(StrictHeadMatching):
    """ A variation of SHM that no check compatible modifiers. """

    sort_name = "SHMB"

    ONLY_FIRST_MENTION = True
    NO_PRONOUN = True
    DISCOURSE_SALIENCE = True
    NO_STOP_WORDS = True

    def word_inclusion(self, entity, mention, candidate_entities):
        """ Void this filtering
        @param entity: Irrelevant
        @param mention: Irrelevant
        @param candidate_entities: Irrelevant
        @return: Always True
        """
        return True

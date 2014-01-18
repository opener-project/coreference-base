# coding=utf-8
""" Al the sieves that are relatid with the same head coreference.

"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ...multisieve.sieves.base import Sieve
from ...resources.dictionaries import stopwords
from ...resources.tagset import pos_tags


class StrictHeadMatching(Sieve):
    """ A relative pronoun is referent to the NP that modified."""
    sort_name = "SHM"
    #Filter options
    ONLY_FIRST_MENTION = True
    NO_PRONOUN = True
    DISCOURSE_SALIENCE = True
    NO_STOP_WORDS = True

    def are_coreferent(self, entity, mention, candidate):
        """ Check if the candidate and the entity are related by checking heads.
        @param entity: The entity cluster.
        @param mention: The current mention of the entity.
        @param candidate: The mention candidate to the cluster.
        @return: True or false
        """

        if not Sieve.are_coreferent(self, entity, mention, candidate):
            return False

        candidate_entities = [[self.graph.node[candidate_mention] for candidate_mention in candidate_entity]
                              for candidate_entity in self.entities_of_a_mention(candidate)]
        entity_mentions = [self.graph.node[m] for m in entity]

        if self.i_within_i(mention_a=mention, mention_b=candidate):
            self.debug("LINK FILTERED I within I construction: %s",
                       candidate["form"])
            return False
        if not self.entity_head_match(mention=mention, candidate_entities=candidate_entities):
            self.debug("LINK FILTERED No head match: %s",
                       candidate["form"])
            return False
        if not self.word_inclusion(entity=entity_mentions, mention=mention, candidate_entities=candidate_entities):
            self.debug("LINK FILTERED No word inclusion: %s",
                       candidate["form"])
            return False
        if not self.compatible_modifiers_only(entity=entity_mentions, candidate_entities=candidate_entities):
            self.debug("LINK FILTERED Incompatible modifiers: %s",
                       candidate["form"])
            return False
        self.debug("LINK MATCH: %s",  candidate["form"])
        return True

    def get_head_word_form(self, element):
        """ Get the head of a chunk

        @param element: A syntactic element
        @return: String, the form of the word.
        """
        head = self.graph_builder.get_head_word(element)
        # if head is None return None. If not return head form
        return head["form"]

    def get_modifiers(self, element):
        """ Get the forms of the modifiers of a syntactic element.

        @param element: A syntactic element
        @return: List of strings, the forms of the words that appears in the element and are mods.
        """
        element_head = self.get_head_word_form(element)
        all_mods = set([word["form"].lower() for word in self.graph_builder.get_words(element)
                        if pos_tags.mod_forms(word["pos"])]) - set(element_head)
        return all_mods

    def get_all_word(self, element):
        """ Get the forms of every word of a syntactic element.

        @param element: A syntactic element
        @return: List of strings, the forms of the words that appears in the element.
        """
        all_words = set([word["form"].lower() for word in self.graph_builder.get_words(element)])
        return all_words

    def entity_head_match(self, mention, candidate_entities):
        """Checks if the head word form of the mention is equals to the head word of any of the candidate entity
        mentions.
        @param mention: The
        @param candidate_entities:
        @return True of False
        """
        mention_head_word = self.get_head_word_form(mention).lower()
        for candidate_entity in candidate_entities:
            for candidate_entity_mention in candidate_entity:
                if self.get_head_word_form(candidate_entity_mention).lower() == mention_head_word:
                    return True
        return False

    def word_inclusion(self, entity, mention, candidate_entities):
        """ Check if every word in the candidate entity(s) is included in the mention words. Except stop words.
        @param entity: The entity cluster.
        @param mention: The current mention of the entity.
        @param candidate_entities: all the entities where the candidate appears.
        @return: True or false
        """
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
        @param entity: The entity cluster.
        @param candidate_entities: all the entities where the candidate appears.
        @return: True or false
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


class StrictHeadMatchingVariantA(StrictHeadMatching):
    """ A variation of SHM that no check compatible modifiers. """

    sort_name = "SHMA"

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

    def word_inclusion(self, entity, mention, candidate_entities):
        """ Void this filtering
        @param entity: Irrelevant
        @param mention: Irrelevant
        @param candidate_entities: Irrelevant
        @return: Always True
        """
        return True

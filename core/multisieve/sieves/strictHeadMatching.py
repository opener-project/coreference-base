from multisieve.sieves.base import Sieve
from multisieve.dictionaries import mod_forms, stop_words

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '14-11-2012'


class StrictHeadMatching(Sieve):
    """ A relative pronoun is referent to the NP that modified."""

    sort_name = "SHM"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        return self.mention_type[mention] != "pronoun_mention"

    def get_head_word_form(self, chunk):
        """ Get the head of a chunk
        """
        head = self.tree_utils.get_chunk_head_word(chunk)
        if head:
            return self.mention_form[head]
        return None

    def get_modifiers(self, chunk):
        """ Get the chunk forms list that are related to a chunk by a mod dependency.
        """
        chunk_head = self.get_head_word_form(chunk)
        all_mods = set([self.mention_form[word] for word in self.tree_utils.get_chunk_words(chunk)
                        if self.mention_pos[word] in mod_forms]) - set(chunk_head)
        return all_mods

    def included(self, small_chunk, big_chunk):
        chunk = small_chunk
        while chunk:
            if chunk == big_chunk:
                return True
            chunk = self.tree_utils.get_syntactic_parent(chunk)
        return False

    def entity_head_match(self, entity, candidate):
        """Checks if the head of the candidate is the head word of any mention of the entity.
        """
        candidate_head = self.get_head_word_form(candidate)
        if candidate_head is None:
            return False
        for mention in entity:
            head_mention = self.get_head_word_form(mention)
            if head_mention and head_mention == candidate_head:
                return True
        return False

    def word_inclusion(self, entity, mention, candidate):
        # Change mention / candidates form
        candidate_words = set([self.mention_form[word]
                               for candidate_entity in self.entities_of_a_mention(candidate)
                               for candidate_mention in candidate_entity
                               for word in self.tree_utils.get_chunk_words(candidate_mention)])
        entity_words = set([self.mention_form[word]
                            for n_mention in entity for word in self.tree_utils.get_chunk_words(n_mention)])
        return len((entity_words - candidate_words) - stop_words) == 0

    def compatible_modifiers_only(self, entity, mention, candidate):
        """Check if all the modifiers of the candidate appears in the first mention of the entity.
        """
        candidate_modifiers = self.get_modifiers(candidate)
        mention_modifiers = self.get_modifiers(mention)
        return len(mention_modifiers - candidate_modifiers) == 0

    def i_within_i(self, entity, mention, candidate):
        """ Check if the  mention and candidate aren't in a i-within-i construction.
        """
        #TODO Aren't appositive
        # Ya detectados en el sieve 1
        #TODO Aren't Relative pronouns
        # Idem
        #TODO One is included in the other
        if self.tree_utils.same_sentence(mention, candidate):
            if self.included(mention, candidate) or self.included(candidate, mention):
                return True
        return False

    def are_coreferent(self, entity, index, candidate):
        return self.entity_head_match(entity, candidate) and \
            self.word_inclusion(entity, entity[index], candidate) and \
            self.compatible_modifiers_only(entity, entity[index], candidate) and \
            not(self.i_within_i(entity, entity[index], candidate))






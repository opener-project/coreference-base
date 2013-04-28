from multisieve.sieves.base import Sieve
import resources.dictionaries as dictionaries
from resources.tagset import pos_tags, constituent_tags, ner_tags


class RoleAppositiveConstruction(Sieve):

    sort_name = "RAC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def is_role_apositive(self, candidate, mention):

        candidate_head = self.get_terminal_head(candidate)
        if self.mention_pos[candidate_head] not in pos_tags.nouns:
            return False

        candidate_syntactic_father = self.graph_builder.get_syntactic_parent(candidate)
        if self.mention_tag[candidate_syntactic_father] != constituent_tags.noun_phrase:
            return False

        return mention == self.graph_builder.get_chunk_head(candidate_syntactic_father)

    def validate(self, mention):
        """Entity must be in appositive construction"""
        # constrain(a)
        if (self.mention_ner[mention] not in ner_tags.person_ner_tag) or \
                (self.mention_ner[self.get_terminal_head(mention=mention)].upper() not in dictionaries.person_ner_tag):
            return False
        return True

    def are_coreferent(self, entity, index, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        # (b) and (c) constrains
        if self.mention_gender[candidate] == "NEUTRAL" or self.mention_animacy[candidate] == "INANIMATE":
            return False

        return self.is_role_apositive(candidate, entity[index])


class AcronymMatch(Sieve):
    """ A demonym is coreferent to their location."""

    sort_name = "AMC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Any mention except pronouns.
        """
        return self.mention_type[mention] != "pronoun_mention"

    def are_coreferent(self, entity, index, candidate):
        """ Mention and candidate are one demonym of the other."""
        #TODO limpiar acronimos
        #TODO No tiene en cuenta los posibles plurales
        candidate_form = self.mention_form[candidate]
        candidate_type = self.mention_type[candidate]
        mention_form = self.mention_form[entity[index]]

        if candidate_type == "pronoun_mention":
            return False
        if len(candidate_form) > len(mention_form):
            sort, large = mention_form, candidate_form
        else:
            sort, large = candidate_form, mention_form
        generated_acronyms = (filter(str.isupper, large),)
        return sort in generated_acronyms


class RelativePronoun(Sieve):
    """ A relative pronoun is referent to the NP that modified."""

    sort_name = "RPC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be relative pronoun."""
        return self.mention_form[mention] in pos_tags.relative_pronouns

    def are_coreferent(self, entity, index, candidate):
        """ Candicate is the NP that the relative pronoun modified."""
        candidate_tag = self.mention_tag[candidate]
        # TODO only NP candidates?
        if candidate_tag != constituent_tags.noun_phrase:
            return False
            # TODO is the only valid conection?
        return self.tree_utils.is_relative_pronoun(candidate, entity[index])


class PredicativeNominativeConstruction(Sieve):
    """ The mention and the candidate are in a subject-object copulative relation ."""
    sort_name = "PNC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be relative pronoun."""
        # The head is in a copula dependency
        # The mention is nominal o pronominal

        return self.tree_utils.is_predicative_nominative(mention)

    def are_coreferent(self, entity, index, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        mention_parent = self.tree_utils.get_syntactic_parent(entity[index])
        siblings = self.tree_utils.get_sibling(mention_parent)
        mention_index = siblings.index(mention_parent)

        if siblings[mention_index - 1] == candidate:
            return True
        return False


class AppositiveConstruction(Sieve):
    """Two nominal mentions  in an appositive construction are coreferent
    """
    sort_name = "ACC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be in appositive construction"""
        return self.tree_utils.is_appositive_construction(mention=mention)

    def are_coreferent(self, entity, index, candidate):
        """Candidate is The NP that cover the apossitive construction."""
        return candidate == self.tree_utils.get_syntactic_parent(entity[index])
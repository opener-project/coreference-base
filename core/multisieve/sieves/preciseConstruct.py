from multisieve.sieves.base import Sieve
import resources.dictionaries as dictionaries
from resources.tagset import pos_tags, constituent_tags, ner_tags


class AppositiveConstruction(Sieve):
    """Two nominal mentions  in an appositive construction are coreferent
    """
    sort_name = "ACC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be in appositive construction"""
        # If mention is NE use their constituent for syntax checks
        if mention["type"] == "named_entity":
            mention_constituent = mention["constituent"]
        else:
            mention_constituent = mention

        return super(AppositiveConstruction, self).validate(mention) and \
            self.tree_utils.is_appositive_construction(mention=mention_constituent)

    def are_coreferent(self, entity, mention, candidate):
        """Candidate is The NP that cover the appositive construction."""
        # If candidate or mention are NE use their constituent as mentions
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if mention["type"] == "named_entity":
            mention = mention["constituent"]
        return candidate == self.tree_utils.get_syntactic_parent(entity[mention])


class RoleAppositiveConstruction(Sieve):

    sort_name = "RAC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be in appositive construction"""
        # constrain(a) The mention must be labeled as person
        return super(RoleAppositiveConstruction, self).validate(mention) and ner_tags.person(mention["ner"])

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        # (b) and (c) constrains The candidate must be animate and can not be neutral.
        if candidate["gender"] == "NEUTRAL" or candidate["animacy"] == "INANIMATE":
            return False
        return self.tree_utils.is_role_appositive(candidate, mention)


class AcronymMatch(Sieve):
    """ A demonym is coreferent to their location."""

    sort_name = "AMC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Any mention except pronouns.
        """
        return super(AcronymMatch, self).validate(mention) and mention["mention"] != "pronoun_mention"

    def are_coreferent(self, entity, mention, candidate):
        """ Mention and candidate are one demonym of the other."""
        #TODO limpiar acronimos
        #TODO No tiene en cuenta los posibles plurales
        candidate_form = candidate["form"]
        candidate_type = candidate["mention"]
        mention_form = mention["form"]

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
        return mention["form"] in dictionaries.pronouns.relative

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        candidate_tag = candidate["tag"]
        # TODO is the only valid precedent
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if candidate_tag != constituent_tags.noun_phrase:
            return False
        return self.tree_utils.is_relative_pronoun(candidate, mention)


class PredicativeNominativeConstruction(Sieve):
    """ The mention and the candidate are in a subject-object copulative relation ."""
    sort_name = "PNC"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be relative pronoun."""
        # If mention is NE use their constituent
        if mention["type"] == "named_entity":
            mention_constituent = mention["constituent"]
        else:
            mention_constituent = mention
        return super(PredicativeNominativeConstruction, self).validate(mention) and \
            self.tree_utils.is_predicative_nominative(mention_constituent)

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the subject of the predicative-nominative relation of the mention."""
        # This sieve is full syntactic related so in NE whe use artificial constituent
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if mention["type"] == "named_entity":
            mention = mention["constituent"]
        # TODO TALK with Rodrigo about THIS
        if mention["root"] == candidate["root"]:
            # "S < (NP=m1 $.. (VP < ((/VB/ < /^(am|are|is|was|were|'m|'re|'s|be)$/) $.. NP=m2)))";
            # "S < (NP=m1 $.. (VP < (VP < ((/VB/ < /^(be|been|being)$/) $.. NP=m2))))";
            mention_parent = self.tree_utils.get_syntactic_parent(mention)
            aditional_parent = self.tree_utils.get_syntactic_parent(mention_parent)
            if constituent_tags.verb_phrases(aditional_parent["tag"]):
                siblings = self.tree_utils.get_syntactic_sibling(aditional_parent)
            else:
                siblings = self.tree_utils.get_syntactic_sibling(mention_parent)
            # or siblings[X] == candidate?
            if candidate in siblings:
                return True
        return False


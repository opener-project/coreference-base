# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ...multisieve.sieves.base import Sieve
from ...resources import dictionaries
from ...resources.tagset import pos_tags, constituent_tags, ner_tags


class AppositiveConstruction(Sieve):
    """Two nominal mentions  in an appositive construction are coreferent
    """
    sort_name = "ACC"
    ONLY_FIRST_MENTION = False
    NO_PRONOUN = False
    DISCOURSE_SALIENCE = True
    NO_STOP_WORDS = False

    def __init__(self, multi_sieve_processor, options):
        super(self.__class__, self).__init__(multi_sieve_processor, options)
        self.filter_apposition = "CONSTRUCT_FILTER_APPOSITION" in options

    def validate(self, mention, mention_index):
        """Entity must be in appositive construction"""
        if not super(self.__class__, self).validate(mention, mention_index):
            return False
        return self.tree_utils.is_appositive_construction_child(constituent=mention)

    def are_coreferent(self, entity, mention, candidate):
        """Candidate is The NP that cover the appositive construction."""
        # If candidate or mention are NE use their constituent as mentions
        if self.is_pronoun(candidate) and self.is_pronoun(mention):
            return False

        if not self.agree_attributes(entity=entity, candidate=candidate):
            return False

        if self.is_location(mention):
            return False
        # Check the apposition
        if candidate["constituent"] == self.tree_utils.get_syntactic_parent(mention["constituent"]):
            if self.filter_apposition:
                mention["purge"] = True
            self.logger.debug("APPOSITIVE CONSTRUCTION MATCH: %s %s", mention["form"], candidate["form"])
            return True
        return False


class RoleAppositiveConstruction(Sieve):

    sort_name = "RAC"
    DISCOURSE_SALIENCE = False
    ONLY_FIRST_MENTION = False

    def __init__(self, multi_sieve_processor, options):
        super(self.__class__, self).__init__(multi_sieve_processor, options)
        self.filter_role_apposition = "CONSTRUCT_FILTER_ROLE_APPOSITION" in options

    def validate(self, mention, mention_index):
        """Entity must be in appositive construction"""
        # constrain(a) The mention must be labeled as person
        return super(self.__class__, self).validate(mention, mention_index) and \
               ner_tags.person(self.graph_builder.get_ner(mention))

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        if not super(self.__class__, self).are_coreferent(entity, mention, candidate):
            return False
        # (b) and (c) constrains The candidate must be animate and can not be neutral.
        if candidate["gender"] == "NEUTRAL" or candidate["animacy"] == "INANIMATE":
            return False
        if self.tree_utils.is_role_appositive(candidate, mention):
            if self.filter_role_apposition:
                mention["purge"] = True
            self.logger.debug("ROLE APPOSITIVE CONSTRUCTION MATCH: %s %s", mention["form"], candidate["form"])
            return True
        return False


class AcronymMatch(Sieve):
    """ A demonym is coreferent to their location."""

    sort_name = "AMC"
    DISCOURSE_SALIENCE = False
    ONLY_FIRST_MENTION = False

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
    DISCOURSE_SALIENCE = False
    ONLY_FIRST_MENTION = False
    NO_PRONOUN = False

    def validate(self, mention, mention_index):
        """Entity must be relative pronoun."""
        return super(self.__class__, self).validate(mention, mention_index) and \
               mention["form"] in dictionaries.pronouns.relative

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        candidate_tag = "tag" in candidate and candidate["tag"]
        # TODO is the only valid precedent
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if not constituent_tags.noun_phrases(candidate_tag):
            return False
        return self.tree_utils.is_relative_pronoun(candidate, mention)


class PredicativeNominativeConstruction(Sieve):
    """ The mention and the candidate are in a subject-object copulative relation ."""
    sort_name = "PNC"
    DISCOURSE_SALIENCE = False
    ONLY_FIRST_MENTION = False

    def __init__(self, multi_sieve_processor, options):
        super(self.__class__, self).__init__(multi_sieve_processor, options)
        self.filter_predicative_nominative = "CONSTRUCT_FILTER_PREDICATIVE_NOMINATIVE" in options

    def validate(self, mention, mention_index):
        """Entity must be relative pronoun."""
        # If mention is NE use their constituent
        if mention["type"] == "named_entity":
            mention_constituent = mention["constituent"]
        else:
            mention_constituent = mention
        return super(PredicativeNominativeConstruction, self).validate(mention, mention_index) and \
            self.tree_utils.is_predicative_nominative(mention_constituent)

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the subject of the predicative-nominative relation of the mention."""
        # This sieve is full syntactic related so in NE whe use artificial constituent
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if mention["type"] == "named_entity":
            mention = mention["constituent"]
        if self.graph_builder.same_sentence(mention, candidate):
            # S < (NP=m1 $.. (VP < ((/VB/ < /^(am|are|is|was|were|'m|'re|'s|be)$/) $.. NP=m2)))
            # S < (NP=m1 $.. (VP < (VP < ((/VB/ < /^(be|been|being)$/) $.. NP=m2))))
            mention_parent = self.graph_builder.get_syntactic_parent(mention)
            mention_grandparent = self.graph_builder.get_syntactic_parent(mention_parent)
            if constituent_tags.verb_phrases(mention_grandparent["tag"]):
                enclosing_verb_phrase = mention_parent
            else:
                return False
            if constituent_tags.verb_phrases(mention_grandparent["tag"]):
                enclosing_verb_phrase = mention_grandparent
            if self.graph_builder.get_syntactic_sibling(mention)[0]["form"] not in dictionaries.verbs.copulative:
                return False
            siblings = []
            enclosing_verb_phrase_id = enclosing_verb_phrase["id"]
            for sibling in self.graph_builder.get_syntactic_sibling(enclosing_verb_phrase):
                if sibling["id"] == enclosing_verb_phrase_id:
                    break
                siblings.append(sibling)
            siblings = [sibling["id"] for sibling in siblings]
            # or siblings[X] == candidate?
            if candidate["id"] in siblings:
                if self.filter_predicative_nominative:
                    mention["purge"] = True
                return True
        return False


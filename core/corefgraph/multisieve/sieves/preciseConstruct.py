# coding=utf-8
""" The sieves that check construction that denotes coreference.
"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ...multisieve.sieves.base import Sieve
from ...resources import dictionaries
from ...resources.tagset import constituent_tags, ner_tags


class AppositiveConstruction(Sieve):
    """Two nominal mentions  in an appositive construction are coreferent
    """
    sort_name = "ACC"
    #Filter options
    ONLY_FIRST_MENTION = False
    NO_PRONOUN = False
    DISCOURSE_SALIENCE = True
    NO_STOP_WORDS = False

    def __init__(self, multi_sieve_processor, options):
        super(self.__class__, self).__init__(multi_sieve_processor, options)
        self.filter_apposition = "CONSTRUCT_FILTER_APPOSITION" in options

    def validate(self, mention, mention_index):
        """Entity must be in appositive construction.

        :param mention: The mention to check.
        :param mention_index: Index of the mention inside entity:
       """
        if not super(self.__class__, self).validate(mention, mention_index):
            return False
        if self.tree_utils.is_appositive_construction_child(constituent=mention):
            return True
        self.debug("MENTION FILTERED Not in appositive construction: %s", mention["form"])
        return False

    def are_coreferent(self, entity, mention, candidate):
        """Candidate is The NP that cover the appositive construction.

        :param candidate: The candidate that may corefer the entity.
        :param mention: The selected mention to represent the entity.
        :param entity: The entity that is going to be evaluated.
        """
        # If candidate or mention are NE use their constituent as mentions
        if self.is_pronoun(candidate) and self.is_pronoun(mention):
            self.debug("LINK IGNORED are pronouns: %s", candidate["form"])
            return False

        if not self.agree_attributes(entity=entity, candidate=candidate):
            self.debug("LINK IGNORED attributes disagree:%s", candidate["form"])
            return False

        if self.is_location(mention):
            self.debug("LINK IGNORED is a location: %s %s", candidate["form"], mention.get("ner", "NO NER "))
            return False
        # Check the apposition
        if candidate["constituent"] == self.tree_utils.get_syntactic_parent(mention["constituent"]):
            if self.filter_apposition:
                self.debug("LINK PURGE link set as purge: %s", candidate["form"])
                mention["purge"] = True
            self.debug("LINK MATCH: %s", candidate["form"])
            return True
        self.debug("LINK IGNORED: %s", candidate["form"])
        return False


class RoleAppositiveConstruction(Sieve):

    sort_name = "RAC"
    #Filter options
    DISCOURSE_SALIENCE = False
    ONLY_FIRST_MENTION = False

    def __init__(self, multi_sieve_processor, options):
        super(self.__class__, self).__init__(multi_sieve_processor, options)
        self.filter_role_apposition = "CONSTRUCT_FILTER_ROLE_APPOSITION" in options

    def validate(self, mention, mention_index):
        """Entity must be in appositive construction"""
        if not super(self.__class__, self).validate(mention, mention_index):
            return False
            # constrain(a) The mention must be labeled as person
        if not ner_tags.person(mention.get("ner", ner_tags.no_ner)):
            self.debug("MENTION FILTERED Not a person: %s %s", mention["form"], mention.get("ner", "NO NER "))
            return False
        return True

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        if not super(self.__class__, self).are_coreferent(entity, mention, candidate):
            return False
        # (b) and (c) constrains The candidate must be animate and can not be neutral.
        if candidate["gender"] == "NEUTRAL":
            self.debug("LINK FILTERED Candidate is neutral: %s %s", candidate["form"], candidate["gender"])
            return False
        if candidate["animacy"] == "INANIMATE":
            self.debug("LINK FILTERED Candidate is inanimate: %s %s", candidate["form"], candidate["animacy"])
            return False
        if self.tree_utils.is_role_appositive(candidate, mention):
            if self.filter_role_apposition:
                mention["purge"] = True
            self.logger.debug("LINK MATCH: %s", mention["form"])
            return True
        self.debug("LINK IGNORED: %s", candidate["form"])
        return False


class AcronymMatch(Sieve):
    """ A demonym is coreferent to their location."""
    #Filter options
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
            self.debug("LINK FILTERED Candidate is not a pronoun: %s %s", candidate_form, candidate_type)
            return False
        if len(candidate_form) > len(mention_form):
            sort, large = mention_form, candidate_form
        else:
            sort, large = candidate_form, mention_form
        generated_acronyms = (filter(str.isupper, large),)
        if sort in generated_acronyms:
            self.logger.debug("ACRONYM MATCH: %s %s", mention["form"], candidate["form"])
            return True
        self.debug("LINK IGNORED: %s", candidate_form)
        return False


class RelativePronoun(Sieve):
    """ A relative pronoun is referent to the NP that modified."""

    sort_name = "RPC"
    #Filter options
    DISCOURSE_SALIENCE = False
    ONLY_FIRST_MENTION = False
    NO_PRONOUN = False

    def validate(self, mention, mention_index):
        """Entity must be relative pronoun."""
        if not super(self.__class__, self).validate(mention, mention_index):
            return False
        if not mention["form"] in dictionaries.pronouns.relative:
            self.debug("MENTION FILTERED Not a relative pronoun: %s ", mention["form"])
            return False
        return True

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate is the NP that the relative pronoun modified."""

        candidate_tag = candidate.get("tag", False)
        if candidate["type"] == "named_entity":
            candidate = candidate["constituent"]
        if mention["type"] == "named_entity":
            mention = mention["constituent"]

        # TODO is the only valid precedent
        if not constituent_tags.noun_phrases(candidate_tag):
            self.debug("LINK FILTERED Candidate is not a noun phrase: %s %s", candidate["form"], candidate_tag)

            return False
        if self.tree_utils.is_relative_pronoun(candidate, mention):
            self.debug("RELATIVE PRONOUN MATCH: %s", candidate["form"])
            return True
        self.debug("LINK IGNORED: %s", candidate["form"])
        return False


class PredicativeNominativeConstruction(Sieve):
    """ The mention and the candidate are in a subject-object copulative relation ."""
    sort_name = "PNC"
    #Filter options
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
        if not super(PredicativeNominativeConstruction, self).validate(mention, mention_index):
            return False
        if not self.tree_utils.is_predicative_nominative(mention_constituent):
            self.debug("MENTION FILTERED Not in a predicative nominative construction: %s ", mention["form"])
            return False
        return True

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
            if constituent_tags.verb_phrases(mention_parent["tag"]):
                enclosing_verb_phrase = mention_parent
            else:
                self.debug("LINK FILTERED No enclosing verb: %s ", candidate["form"])
                return False
            if constituent_tags.verb_phrases(mention_grandparent["tag"]):
                enclosing_verb_phrase = mention_grandparent
            if self.graph_builder.get_syntactic_sibling(mention)[0]["form"] not in dictionaries.verbs.copulative:
                self.debug("LINK FILTERED verb is not copulative: %s ", candidate["form"])
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
                    self.debug("LINK MATCH: %s", candidate["form"])
                return True
        self.debug("LINK IGNORED: %s ", candidate["form"])
        return False


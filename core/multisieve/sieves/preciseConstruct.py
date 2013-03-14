from multisieve.sieves.base import Sieve
import multisieve.dictionaries as dictionaries


class RoleAppositiveConstruction(Sieve):
    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def is_role_apositive(self, candidate, mention):

        candidate_head = self.get_terminal_head(candidate)
        if self.mention_pos[candidate_head] not in dictionaries.nouns_pos:
            return False

        candidate_syntactic_father = self.graph_builder.get_syntactic_parent(candidate)
        if self.mention_tag[candidate_syntactic_father] != dictionaries.noun_phrase_tag:
            return False

        return mention == self.graph_builder.get_chunk_head(candidate_syntactic_father)

    def validate(self, mention):
        """Entity must be in appositive construction"""
        # constrain(a)
        if (self.mention_ner[mention] not in dictionaries.person_ner_tag) or \
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

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be relative pronoun."""
        return self.mention_form[mention] in dictionaries.relative_pronoun

    def are_coreferent(self, entity, index, candidate):
        """ Candicate is the NP that the relative pronoun modified."""
        candidate_tag = self.mention_tag[candidate]
        # TODO only NP candidates?
        if candidate_tag != dictionaries.noun_phrase_tag:
            return False
            # TODO is the only valid conection?
        return set(filter(lambda X: self.mention_tag[X] in
                            dictionaries.subordinated_clause_tag, entity[index].in_neighbours())).intersection(
                                set(filter(lambda X: self.mention_tag[X] in
                                    dictionaries.subordinated_clause_tag, candidate.out_neighbours())))


class PredicativeNominativeConstruction(Sieve):
    """ The mention and the candidate are in a subject-object copulative relation ."""

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be relative pronoun."""
        # The head is in a copula dependency
        # The mention is nominal o pronominal

        siblings = self.get_sibling(mention)
        mention_index = siblings.index(mention)

        if mention_index > 0 and \
                self.mention_form[siblings[mention_index - 1]].split()[-1] in dictionaries.copulative_verbs:
            return True
        return False

    def are_coreferent(self, entity, index, candidate):
        """ Candidate is the NP that the relative pronoun modified."""
        mention_parent = self.graph_builder.get_syntactic_parent(entity[index])
        siblings = self.get_sibling(mention_parent)
        mention_index = siblings.index(mention_parent)

        if siblings[mention_index - 1] == candidate:
            return True
        return False


class AppositiveConstruction(Sieve):
    """Two nominal mentions  in an appositive construction are coreferent
    """

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Entity must be in appositive construction"""
        siblings = self.get_sibling(mention)

        for sibling in siblings:
            if self.mention_tag[sibling] == dictionaries.conjuntion_tag:
                return False

        if len(siblings) == 3:
            return self.mention_tag[siblings[0]] == dictionaries.noun_phrase_tag and self.mention_form[
                siblings[1]] == ","
        elif len(siblings) > 3:
            return self.mention_tag[siblings[0]] == dictionaries.noun_phrase_tag and self.mention_form[
                siblings[1]] == "," \
                and self.mention_form[siblings[3]] == ","
        else:
            return False

    def are_coreferent(self, entity, index, candidate):
        """Candidate is The NP that cover the apossitive construction."""
        return candidate == self.graph_builder.get_syntactic_parent(entity[index])
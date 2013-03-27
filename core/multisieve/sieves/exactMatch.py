from multisieve.sieves.base import Sieve

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class ExactMatch(Sieve):
    """ To mentions are coreferent if their surfaces are equals."""
    sort_name = "EM"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Any mention except pronouns.
        """
        return self.mention_type[mention] != "pronoun_mention"

    def are_coreferent(self, entity, index, candidate):
        """ Candidate an primary mention have same form
        """
        return self.mention_form[entity[index]].lower() == self.mention_form[candidate].lower()



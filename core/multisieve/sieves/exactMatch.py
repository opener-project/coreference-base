from multisieve.sieves.base import Sieve

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class ExactMatch(Sieve):
    """ Two mentions are coreferent if their surfaces are equals."""
    sort_name = "EM"

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def validate(self, mention):
        """Any mention except pronouns.
        """
        return mention["mention"] != "pronoun_mention"

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate an primary mention have same form
        """
        return mention["form"].lower() == candidate["form"].lower()



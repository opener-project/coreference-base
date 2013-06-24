from multisieve.sieves.base import Sieve
from resources.demonym import locations_and_demonyms, demonym_by_location

__author__ = 'josubg'


class DemonymMatch(Sieve):
    """ A demonym is coreferent to their location."""

    def __init__(self, multi_sieve_processor):
        Sieve.__init__(self, multi_sieve_processor)

    def are_coreferent(self, entity, mention, candidate):
        """ Mention and candidate are one demonym of the other."""
        candidate_form = candidate["form"].lower()
        mention_form = mention["form"].lower()
        return (candidate_form in locations_and_demonyms) and \
               ((mention_form in demonym_by_location and
                 mention_form in demonym_by_location[mention_form]) or
                (candidate_form in demonym_by_location and
                 mention_form in demonym_by_location[candidate_form]))

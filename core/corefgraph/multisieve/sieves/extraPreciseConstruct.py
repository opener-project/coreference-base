# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ...resources.demonym import locations_and_demonyms, demonym_by_location
from ...multisieve.sieves.base import Sieve


class DemonymMatch(Sieve):
    """ A demonym is coreferent to their location."""
    sort_name = "DMC"
    #Filter options
    DISCOURSE_SALIENCE = False
    ONLY_FIRST_MENTION = False

    def are_coreferent(self, entity, mention, candidate):
        """ Mention and candidate are one demonym of the other."""
        if not super(self.__class__, self).are_coreferent(entity, mention, candidate):
            return False
        candidate_form = candidate["form"].lower()
        mention_form = mention["form"].lower()
        if ((candidate_form in locations_and_demonyms) and
                ((mention_form in demonym_by_location and
                 mention_form in demonym_by_location[mention_form]) or
                (candidate_form in demonym_by_location and
                 mention_form in demonym_by_location[candidate_form]))):
            self.debug("LINK MATCH: %s", candidate_form)
            return True
        self.debug("LINK IGNORED: %s ", candidate["form"])
        return False

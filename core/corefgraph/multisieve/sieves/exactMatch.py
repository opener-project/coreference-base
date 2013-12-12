# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ...multisieve.sieves.base import Sieve


class ExactMatch(Sieve):
    """ Two mentions are coreferent if their surfaces are equals."""
    sort_name = "EM"
    #filterin options
    DISCOURSE_SALIENCE = True
    ONLY_FIRST_MENTION = False
    NO_PRONOUN = True
    NO_STOP_WORDS = True

    DEBUG = False

    def are_coreferent(self, entity, mention, candidate):
        """ Candidate an primary mention have same form
        """
        if not super(self.__class__, self).are_coreferent(entity, mention, candidate):
            return False
        candidate_form = candidate["form"].lower()
        for mention_x in entity:
            mention_x_form = self.graph.node[mention_x]["form"].lower()

            if (mention_x_form == candidate_form) or \
                    (mention_x_form + " 's" == candidate_form)or \
                    (mention_x_form == candidate_form + " 's"):
                self._print(mention_x_form, candidate_form)
                return True
        return False

    def _print(self, mention, candidate):
        if self.DEBUG:
            print mention, candidate

# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
""" All the sieves are published here for the multi-sieve system. They are accessible to the multi-sieve system by their
sort name. Also the default sieve pack is defined here.
"""

from . import speakertMatch
from . import stringMatch
from . import preciseConstruct
from . import extraPreciseConstruct
from . import strictHeadMatching
from . import pronoumMatch

sieves = {
    speakertMatch.SpeakerSieve.sort_name:
    speakertMatch.SpeakerSieve,
    stringMatch.ExactStringMatch.sort_name:
    stringMatch.ExactStringMatch,
    stringMatch.RelaxedStringMatch.sort_name:
    stringMatch.RelaxedStringMatch,
    preciseConstruct.AppositiveConstruction.sort_name:
    preciseConstruct.AppositiveConstruction,
    preciseConstruct.RoleAppositiveConstruction.sort_name:
    preciseConstruct.RoleAppositiveConstruction,
    preciseConstruct.AcronymMatch.sort_name:
    preciseConstruct.AcronymMatch,
    preciseConstruct.RelativePronoun.sort_name:
    preciseConstruct.RelativePronoun,
    preciseConstruct.PredicativeNominativeConstruction.sort_name:
    preciseConstruct.PredicativeNominativeConstruction,
    extraPreciseConstruct.DemonymMatch.sort_name:
    extraPreciseConstruct.DemonymMatch,
    strictHeadMatching.StrictHeadMatching.sort_name:
    strictHeadMatching.StrictHeadMatching,
    strictHeadMatching.StrictHeadMatchingVariantA.sort_name:
    strictHeadMatching.StrictHeadMatchingVariantA,
    strictHeadMatching.StrictHeadMatchingVariantB.sort_name:
    strictHeadMatching.StrictHeadMatchingVariantB,
    pronoumMatch.PronounMatch.sort_name:
    pronoumMatch.PronounMatch}

default = sieves.keys()

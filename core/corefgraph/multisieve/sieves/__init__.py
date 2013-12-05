__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from . import speakertMatch
from . import exactMatch
from . import relaxedExactMatch
from . import preciseConstruct
from . import extraPreciseConstruct
from . import strictHeadMatching
from . import pronoumMatch

sieves = {
    speakertMatch.SpeakerSieve.sort_name:
    speakertMatch.SpeakerSieve,
    exactMatch.ExactMatch.sort_name:
    exactMatch.ExactMatch,
    relaxedExactMatch.RelaxedExactMatch.sort_name:
    relaxedExactMatch.RelaxedExactMatch,
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
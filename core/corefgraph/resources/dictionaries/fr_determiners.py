__author__ = 'josubg'

from ..lambdas import equality_checker, list_checker

indefinite_articles = list_checker(("un", "une", "uns", "unes"))

quantifiers = list_checker(("pas", "chaque", "chacun", "chacune", "tout", "aucun", "aucune", "tous", "rien", "assez", "trop"))

partitives = list_checker(("half", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix" , "cent",
    "mille", "million", "milliard", "dizaines", "douzaines", "centaines", "milliers", "millions", "milliards",
    "groupe", "groupes", "bouquet", "pincer", "montant", "totale", "tous", "mile",
    "miles", "livres"))

partitive_particle = equality_checker("de")

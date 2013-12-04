# -*- coding: utf-8 -*-
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'
__date__ = '5/13/13'

from ..lambdas import equality_checker, list_checker

indefinite_articles = list_checker(("un", "una", "uno", "un'"))

quantifiers = list_checker(("niente", "nessun", "nessuno", "nessuna", "tutto", "tutti", "tutte", "tutta", "alcun", "alcuno", "alcuna", "alcuni", "alcune", "ogni", "ognun", "ognuno", "ognuna", "ciascuno", "ciascuna", "abbastanza", "qualche", "qualunque", "qualsiasi", "poco", "pochi", "alquanto", "molti", "molte", "molta", "molto", "tanti", "tante", "tanta", "tanto", "parecchi", "parecchio", "parecchie", "parecchia", "numerosi", "numerose", "vari", "varie", )) 

partitives = list_checker(("metà", "meta'", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove", "dieci" , "cento", "mille", "milioni", "miliardi", "milione", "miliardo", "decine", "decina", "dozzine", "dozzina", "centinaia", "centinaio", "migliaia", "migliaio", "gruppo", "gruppi", "manciata", "manciate", "mucchio", "mucchi", "numero", "numeri", "po'", "pizzico", "pugno", "pugni", "quantità", "quantita'", "totale", "chilometro", "chilometri", "metro", "metri", "centimetro", "centimetri", "millimetro", "millimetri", "km", "chilo", "chili", "kg", "chilogrammo", "chilogrammi", "etto", "etti", "grammo", "grammi"))

partitive_particle = list_checker(("del", "dell'", "dello", "della", "delle", "degli", "dei"))

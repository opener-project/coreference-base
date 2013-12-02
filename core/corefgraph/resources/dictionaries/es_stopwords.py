# coding=utf-8

__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'


stop_words = set((
'unas', 'una', 'unos', 'un', 'del', 'al', 'el', 'la', 'los', 'lo', 'las', 'de', 'en', 'sobre', 'por', 'dentro', 'hacia',
'desde', 'fuera', 'como', 'así', 'tal', 'o', 'y', 'esos', 'esas', 'este', 'esta', 'aquellas', 'aquellos', 'ese', 'esa',
'para', ',', 'es', 'fue', 'era', 'soy', 'eres', 'sido', 'eras'))

non_words = ('ejem', 'ajá', 'hm', 'jo')
invalid_stop_words = ("SA", "SL", "etc", "hm")

invalid_start_words = ("'s", "etc", )
invalid_end_words = ("etc", )
invalid_starts_words = ("",)

location_modifiers = ("",)

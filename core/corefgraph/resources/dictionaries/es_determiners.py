# -*- coding: utf-8 -*-
__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'

from ..lambdas import equality_checker, list_checker

# extracted from Freeling dictionary by looking for DI

indefinite_articles = list_checker((
'alguna', 'algún', 'algunas', 'alguno', 'algunos', 'ambas', 'ambos', 'bastante', 'bastantes', 'cada', 'cualesquier',
'cualquier', 'cuantas', 'cuantos', 'demás', 'demasiada', 'demasiadas', 'demasiado', 'demasiados', 'mucha', 'muchas',
'mucho', 'muchos', 'ninguna', 'ningunas', 'ningún', 'ninguno', 'ningunos', 'otra', 'otras', 'otro', 'otros', 'poca',
'pocas', 'poco', 'pocos', 'sendas', 'sendos', 'tantas', 'tanta', 'tantos', 'tanto', 'todas', 'toda', 'todos', 'todo',
'unas', 'una', 'unos', 'un', 'varias', 'varios'))


#cuantificadores; they overlap with indefinite_articles in Spanish

quantifiers = list_checker((
"no", "nada", "suficientemente", "suficiente", "harto", 'alguna', 'algún', 'algunas', 'alguno', 'algunos', 'ambas',
'ambos', 'bastante', 'bastantes', 'cada', 'cualesquier', 'cualquier', 'cuantas', 'cuantos', 'demás', 'demasiada',
'demasiadas', 'demasiado', 'demasiados', 'mucha', 'muchas', 'mucho', 'muchos', 'ninguna', 'ningunas', 'ningún',
'ninguno', 'ningunos', 'otra', 'otras', 'otro', 'otros', 'poca', 'pocas', 'poco', 'pocos', 'sendas', 'sendos', 'tantas',
'tanta', 'tantos', 'tanto', 'todas', 'toda', 'todos', 'todo', 'unas', 'una', 'unos', 'un', 'varias', 'varios'))

# partitivos (we also include here cardinales and ordinales)

partitives = list_checker((
'grupo', 'grupos', 'equipo', 'algunos', 'cantidad', 'total', 'todo', 'miles', 'kilos', 'kilo', 'medio', 'media',
'cuarto', 'cuarta', 'quinto', 'quinta', 'sexta', 'sexto', 'seisava', 'seisavo', 'séptimo', 'séptima', 'octava',
'octavo', 'novena', 'noveno', 'décima', 'décimo', 'undécimo', 'undécima', 'onceavo', 'onceava', 'duodécima',
'duodécimo', 'doceavo', 'doceava', 'decimosegunda', 'decimosegundo', 'decimotercera', 'decimotercero', 'decimotercer',
'decimatercer', 'treceava', 'treceavo', 'decimocuarta', 'decimocuarto', 'quinceava', 'quinceavo', 'decimoquinto',
'decimoquinta', 'decimosexta', 'decimosexto', 'dieciseisavo', 'dieciseisava', 'decimoséptima', 'decimoséptimo',
'diecisieteava', 'diecisieteavo', 'decimooctava', 'decimoctavo', 'dieciochoavo', 'dieciochoava', 'decimonovena',
'decimonoveno', 'diecinueveava', 'diecinueveavo', 'vigésimo', 'vigésima', 'veinteava', 'veinteavo', 'trigésima',
'trigésimo', 'treintavo', 'treintava', 'cuadragésima', 'cuadragésimo', 'cuarentava', 'cuarentavo', 'quincuagésima',
'quincuagésimo', 'cincuentava', 'cincuentavo', 'sexagésima', 'sexagésimo', 'sesentavo', 'sesentava', 'septuagésima',
'septuagésimo', 'setentavo', 'sententava', 'octogésima', 'octogésimo', 'ochentava', 'ochentavo', 'nonagésima',
'nonagésimo', 'centava', 'centavo', 'centésima', 'centésimo', 'milimésima', ' un', 'uno', 'dos', 'tres', 'cuatro',
'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis',
'diecisiete', 'dieciocho', 'diecinueve', 'veinte', 'veintiuno', 'veintidós', 'veintitrés', 'veinticuatro',
'veinticinco', 'veintiséis', 'veintisiete', 'veintiocho', 'veintinueve', 'treinta', 'cuarenta', 'cincuenta', 'sesenta',
'setenta', 'ochenta', 'noventa', 'cien', 'doscientos', 'doscientas', 'trescientos', 'trescientas', 'cuatrocientas',
'cuatrocientos', 'quinientos', 'quinientas', 'seiscientas', 'seiscientos', 'ochocientas', 'ochocientos', 'novecientas',
'novecientos', 'mil', 'millón', 'millones', 'billón', 'billones'))

partitive_particle = equality_checker("de")

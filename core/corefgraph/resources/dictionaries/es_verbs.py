# coding=utf-8

__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'

# Las formas compuestas no son necesarias
#'ser', estar y parecer

_ser = set(('ser', 'erais', 'éramos', 'eran', 'era', 'era', 'eras', 'eres', 'es', 'fuerais', 'fuéramos', 'fueran', 'fuera', 'fuera', 'fueras', 'fuereis', 'fuéremos', 'fueren', 'fuere', 'fuere', 'fueres', 'fueron', 'fueseis', 'fuésemos', 'fuesen', 'fue', 'fuese', 'fuese', 'fueses', 'fuimos', 'fui', 'fuisteis', 'fuiste', 'seréis', 'seamos', 'seamos', 'sean', 'sean', 'sea', 'sea', 'sea', 'seas', 'sed', 'serían', 'sería', 'serías', 'seriáis', 'seremos', 'ser', 'seráis', 'seríamos', 'serán', 'será', 'seré', 'serás', 'ser', 'sé', 'sido', 'siendo', 'sois', 'somos', 'son', 'soy'))

_estar = set(('estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'estaba', 'estabas', 'estaba', 'estábamos', 'estabais', 'estaban', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaría', 'estaríamos', 'estaríais', 'estarían', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'esté', 'estés', 'esté', 'estemos', 'estéis', 'estén', 'estuviera' 'estuvieras', 'estuviera', 'estuviéramos', 'estuvierais', 'estuvieran' 'estuviese', 'estuvieses', 'estuviese', 'estuviésemos', 'estuvieseis', 'estuviesen' 'estuviere', 'estuvieres', 'estuviere', 'estuviéremos', 'estuviereis', 'estuvieren' 'está', 'esté', 'estemos', 'estad', 'estén', 'estar', 'estando', 'estado'))

_parecer = set(('parezco', 'pareces', 'parece', 'parecemos', 'parecéis', 'parecen','parecía', 'parecías', 'parecía', 'parecíamos', 'parecíais', 'parecían', 'pareceré', 'parecerás', 'parecerá', 'pareceremos', 'pareceréis', 'parecerán', 'parecería', 'parecerías', 'parecería', 'pareceríamos', 'pareceríais', 'parecerían', 'parecí', 'pareciste', 'pareció', 'parecimos', 'parecisteis', 'parecieron', 'parezca', 'parezcas', 'parezca', 'parezcamos', 'parezcáis', 'parezcan', 'pareciera', 'parecieras', 'pareciera', 'pareciéramos', 'parecierais', 'parecieran', 'pareciese', 'parecieses', 'pareciese', 'pareciésemos', 'parecieseis', 'pareciesen', 'pareciere', 'parecieres', 'pareciere', 'pareciéremos', 'pareciereis', 'parecieren', 'parece', 'parezca', 'parezcamos', 'pareced', 'parezcan', 'parecer', 'pareciendo', 'parecido'))

copulative = set()
copulative.union(_ser).union(_estar).union(_parecer)

#TODO RELLENAR
# reporting verbs
reporting = ()

# verbs verbs that denotes a generic you "Tu sabes"
generic_you_verbs = ("saber", )

# Pleonastic verbs
#TODO RELLENAR
#(?:is|was|become|became)/)
pleonastic_verbs = ("es", "era", "became", "become")
#(?:seems|appears|means|follows)
alternative_a_pleonastic_verbs = ("seems", "appears", "means", "follows")
#(?:turns|turned)/)
alternative_b_pleonastic_verbs = ("turns",)

# Rules where these list are used
"NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (ADJP $.. (/S|SBAR/))))"
"NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (ADJP < (/S|SBAR/))))"

"NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (NP < /S|SBAR/)))"
"NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:is|was|become|became)/) $.. (NP $.. ADVP $.. /S|SBAR/)))"

"NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (VP < (VBN $.. /S|SBAR/))))))"

"NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (ADJP $.. (/S|SBAR/))))))"
"NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (ADJP < (/S|SBAR/))))))"

"NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (NP < /S|SBAR/)))))"
"NP < (PRP=m1) $.. (VP < (MD $.. (VP < ((/^V.*/ < /^(?:be|become)/) $.. (NP $.. ADVP $.. /S|SBAR/)))))"

"NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:seems|appears|means|follows)/) $.. /S|SBAR/))"

"NP < (PRP=m1) $.. (VP < ((/^V.*/ < /^(?:turns|turned)/) $.. PRT $.. /S|SBAR/))"

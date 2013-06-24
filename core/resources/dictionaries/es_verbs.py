# coding=utf-8

__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'

# Las formas compuestas no son necesarias
#'ser', estar y parecer Andar y parecer

ser = set(('ser', 'erais', 'éramos', 'eran', 'era', 'era', 'eras', 'eres', 'es', 'fuerais', 'fuéramos', 'fueran', 'fuera', 'fuera', 'fueras', 'fuereis', 'fuéremos', 'fueren', 'fuere', 'fuere', 'fueres', 'fueron', 'fueseis', 'fuésemos', 'fuesen', 'fue', 'fuese', 'fuese', 'fueses', 'fuimos', 'fui', 'fuisteis', 'fuiste', 'seréis', 'seamos', 'seamos', 'sean', 'sean', 'sea', 'sea', 'sea', 'seas', 'sed', 'serían', 'sería', 'serías', 'seriáis', 'seremos', 'ser', 'seráis', 'seríamos', 'serán', 'será', 'seré', 'serás', 'ser', 'sé', 'sido', 'siendo', 'sois', 'somos', 'son', 'soy'))

estar = set(('estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'estaba', 'estabas', 'estaba', 'estábamos', 'estabais', 'estaban', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaría', 'estaríamos', 'estaríais', 'estarían', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'esté', 'estés', 'esté', 'estemos', 'estéis', 'estén', 'estuviera' 'estuvieras', 'estuviera', 'estuviéramos', 'estuvierais', 'estuvieran' 'estuviese', 'estuvieses', 'estuviese', 'estuviésemos', 'estuvieseis', 'estuviesen' 'estuviere', 'estuvieres', 'estuviere', 'estuviéremos', 'estuviereis', 'estuvieren' 'está', 'esté', 'estemos', 'estad', 'estén', 'estar', 'estando', 'estado'))


parecer = set(('parezco', 'pareces', 'parece', 'parecemos', 'parecéis', 'parecen','parecía', 'parecías', 'parecía', 'parecíamos', 'parecíais', 'parecían', 'pareceré', 'parecerás', 'parecerá', 'pareceremos', 'pareceréis', 'parecerán', 'parecería', 'parecerías', 'parecería', 'pareceríamos', 'pareceríais', 'parecerían', 'parecí', 'pareciste', 'pareció', 'parecimos', 'parecisteis', 'parecieron', 'parezca', 'parezcas', 'parezca', 'parezcamos', 'parezcáis', 'parezcan', 'pareciera', 'parecieras', 'pareciera', 'pareciéramos', 'parecierais', 'parecieran', 'pareciese', 'parecieses', 'pareciese', 'pareciésemos', 'parecieseis', 'pareciesen', 'pareciere', 'parecieres', 'pareciere', 'pareciéremos', 'pareciereis', 'parecieren', 'parece', 'parezca', 'parezcamos', 'pareced', 'parezcan', 'parecer', 'pareciendo', 'parecido'))

copulative = ser.union(estar).union(parecer)

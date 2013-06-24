# coding=utf-8
__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'
__date__ = '2013-05-03'

# from Freeling dict (P[PDXITR][123][MFCN]P.*')

plural = set(('ellas', 'ellos', 'las', 'les', 'los', 'mías', 'míos', 'nos', 'nosotras', 'nosotros', 'nuestras', 'nuestros', 'os', 'suyas', 'suyos', 'tuyas', 'tuyos', 'ustedes', 'vosotras', 'vosotros', 'vuestras', 'vuestros'))

# from Freeling dict P[PDXITR][123][MFCN]S.*'

singular = set(('conmigo','contigo','él', 'ella', 'la', 'le', 'lo', 'me', 'mía', 'mí', 'mío', 'nuestra', 'nuestro', 'nuestro', 'suya', 'suyo', 'suyo', 'te', 'ti', 'tú', 'tuya', 'tuyo', 'tuyo', 'usted', 'vos', 'vuestra', 'vuestro', 'vuestro', 'yo'))

# from Freeling dict P[PDXITR][123]F.*'

female = set(('ella', 'ellas', 'la', 'las', 'mía', 'mías', 'nosotras', 'nuestra', 'nuestras', 'suyas', 'suya', 'tuyas', 'tuya', 'vosotras', 'vuestras', 'vuestra'))

# from Freeling dict P[PDXITR][123]M.*

male = set(('él', 'ellos', 'lo', 'los', 'mío', 'míos', 'nosotros', 'nuestro', 'nuestros', 'suyos', 'suyo', 'tuyos', 'tuyo', 'vosotros', 'vuestros', 'vuestro'))

# from Freeling dict P[PDXITR][123][CN].*

neutral = set(('conmigo', 'consigo', 'contigo', 'le', 'les', 'lo', 'me', 'mía', 'mío', 'nos', 'nuestro', 'os', 'se', 'sí', 'suyo', 'te', 'ti', 'tú', 'tuyo', 'ustedes', 'usted', 'vos', 'vuestro', 'yo'))

# from Freeling dict P[PDXITR][123].* and manually remove the ones used for inanimate too

animate = set (('contigo', 'él', 'ella', 'ellas', 'ellos', 'le', 'les', 'me', 'mí', 'nos', 'nosotras', 'nosotros', 'os', 'te', 'ti', 'tí', 'ustedes', 'usted', 'vosotras', 'vosotros', 'vos', 'yo'))

# from Freeling dict P[PDXITR][123].* and manually removing the ones used for animate too

inanimate = set(('lo', 'los'))

animacy_unknown = set()

# from Freeling dict PI.*

indefinite = set(('algo', 'alguien', 'alguna', 'algunas', 'alguno', 'algunos', 'ambas', 'ambos', 'bastante', 'bastantes', 'cual', 'cualesquiera', 'cualquiera', 'demás', 'demasiada', 'demasiadas', 'demasiado', 'demasiados', 'media', 'medias', 'medio', 'medios', 'misma', 'mismas', 'mismo', 'mismos', 'mucha', 'muchas', 'mucho', 'muchos', 'nada', 'nadie', 'naide', 'ninguna', 'ningunas', 'ninguno', 'ningunos', 'otra', 'otras', 'otro', 'otros', 'poca', 'pocas', 'poco', 'pocos', 'quienesquiera', 'quienquiera', 'tantas', 'tanta', 'tantos', 'tanto', 'todas', 'toda', 'todos', 'todo', 'unas', 'una', 'unos', 'uno', 'varias', 'varios'))

# from Freeling dict PR.*

relative = set(('adonde', 'como', 'cual', 'cuales', 'cuando', 'cuanta', 'cuantas', 'cuanto', 'cuantos', 'cuya', 'cuyas', 'cuyo', 'cuyos', 'donde', 'que', 'quienes', 'quien'))

others = ()

# what about the relatives? what about the other pronouns present in dcoref?

all = plural.union(singular).union(female).union(male).union(neutral).union(animate).union(inanimate).union(others)


## #tonicos
## tonico_plural_masculino = ("nosotros", "vosotros", "ellos")
## tonico_plural_femenino = ("nosotras", "vosotras", "ellas")
## tonico_plural_desconocido = ("ustedes", "sí", "consigo",)

## tonico_singular_masculino =("él",)
## tonico_singular_femenino = ("ella",)
## tonico_singular_neutro = ("ello",)
## tonico_singular_desconocizo = ("yo", "mí", "conmigo", "tú", "vos", "usted" ,"ti", "contigo", "sí", "consigo")

## tonico_plural = tonico_plural_desconocido + tonico_plural_femenino + tonico_plural_masculino
## tonico_singular = tonico_singular_desconocizo + tonico_singular_femenino + tonico_singular_masculino \
##                     + tonico_singular_neutro
## tonico_masculino = tonico_singular_masculino + tonico_plural_masculino
## tonico_femenino = tonico_singular_femenino + tonico_plural_femenino
## tonico_neutro = tonico_singular_neutro
## tonico_desconocido = tonico_plural_desconocido + tonico_singular_desconocizo

## #atonos
## atono_plural_masculino = ("les",)
## atono_plural_femenino = ("las",)
## atono_plural_neutro = ("los",)
## atono_plural_desconocido = ("nos", "os", "se",)

## atono_singular_masculino = ("le",)
## atono_singular_femenino = ("la",)
## atono_singular_neutro = ("lo",)
## atono_singular_desconocido= ("me", "te", "se", "se")

## atono_plural = atono_plural_masculino + atono_plural_femenino + atono_plural_neutro + atono_plural_desconocido
## atono_singular = atono_singular_masculino + atono_singular_femenino + atono_singular_neutro \
##                     + atono_singular_desconocido

## atono_masculino = atono_plural_masculino + atono_singular_masculino
## atono_femenino = atono_plural_femenino + atono_singular_femenino
## atono_neutro = atono_plural_neutro + atono_singular_neutro
## atono_desconocido = atono_plural_desconocido + atono_singular_desconocido

## #reflexivos
## reflexivo_plural =("nos", "os", "se")
## reflexivo_singular = ("me", "te","se",)

## reflexivo_desconocido = reflexivo_plural + reflexivo_singular

## #reciproco
## reciproco = ("nos", "os", "se")

## reciproco_plural = reciproco
## reciproco_desconocido = reciproco

## #Posesivos no incluidos

## #demostrativos
## demostrativo_plural_masculino = ("estos", "esos", "aquellos")
## demostrativo_plural_femenino = ("estas", "esas", "aquellas")

## demostrativo_singular_masculino = ("este", "ese", "aquel",)
## demostrativo_singular_femenino = ("esta", "esa","aquella",)
## demostrativo_singular_neutro = ("esto", "eso", "aquello")

## demostrativo_plural = demostrativo_plural_masculino + demostrativo_plural_femenino
## demostrativo_singular = demostrativo_singular_masculino + demostrativo_singular_femenino + demostrativo_singular_neutro

## demostrativo_masculino = demostrativo_plural_masculino + demostrativo_singular_masculino
## demostrativo_femenino = demostrativo_plural_femenino + demostrativo_singular_femenino
## demostrativo_neutro = demostrativo_singular_neutro

## #relativos:
## relativo_plural = ("cuales", "quienes", "cuyos")
## relativo_singular = ("que", "cual", "donde", "quien", "cuyo")

## relativo_desconocido = relativo_plural + relativo_singular

## #indefinidos
## indefinido_plural_masculino = ("unos", "algunos", "ningunos", "pocos", "escasos", "muchos", "demasiados", "todos",
##                                 "varios", "otros", "mismos", "tantos")
## indefinido_plural_femenino = ("unas", "algunas", "ningunas", "pocas", "escasas", "muchas", "demasiadas", "todas",
##                                "varias", "otras", "mismas", "tantas")
## indefinido_plural_desconocido = ("cualesquiera", "quinesquiera", "demas")

## indefinido_singular_masculino = ("uno", "alguno", "ninguno", "poco", "escaso", "mucho", "demasiado", "todo", "otro",
##                                   "mismo", "tan", "tanto",)
## indefinido_singular_femenino = ("una", "alguna", "ninguna", "poca", "escasa", "mucha", "demasiada", "toda", "otra",
##                                  "misma", "tanta",)
## indefinido_singular_neutro = ("uno", "algo", "nada", "poco", "escaso", "mucho", "demasiado", "todo", "otro",
##                                "mismo", "tanto", "alguien", "nadie",)
## indefinido_singular_desconocido = ("cualquiera", "quienquiera", "demas")

## indefinido_plural = indefinido_plural_masculino + indefinido_plural_femenino + indefinido_plural_desconocido
## indefinido_singular = indefinido_singular_masculino + indefinido_singular_femenino + indefinido_singular_neutro \
##                         + indefinido_singular_desconocido

## indefinido_femenino = indefinido_plural_femenino + indefinido_singular_femenino
## indefinido_masculino = indefinido_plural_masculino + indefinido_singular_masculino
## indefinido_neutro = indefinido_singular_neutro
## indefinido_desconocido = indefinido_plural_desconocido + indefinido_singular_desconocido

## # feacture groups
## plural = tonico_plural + atono_plural + reflexivo_plural + reciproco_plural + demostrativo_plural + relativo_plural\
##     + indefinido_plural

## singular = tonico_singular + atono_singular + reflexivo_singular + demostrativo_singular + relativo_singular \
##     + indefinido_singular


## female = tonico_femenino + atono_femenino + demostrativo_femenino + indefinido_femenino
## male = tonico_masculino + atono_masculino + demostrativo_masculino + indefinido_masculino
## neutral = tonico_neutro + atono_neutro + demostrativo_neutro + indefinido_neutro

## gender_unknown = tonico_desconocido + atono_desconocido + reflexivo_desconocido + reciproco_desconocido \
##     + relativo_desconocido + indefinido_desconocido


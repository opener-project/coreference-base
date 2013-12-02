# coding=utf-8

import codecs
import re


def expand(gentilicio):
    gentilicios = []
    gentilicio =  gentilicio.replace(",", "").replace("/", "")
    variantes = gentilicio.split(" o ")
    for variante in variantes :
        generos = variante.split(" ")
        if len(generos) > 1:
            generos[1] = generos[1].replace("-", generos[0][:-(len(generos[1])-1)])
        gentilicios.extend(generos)
    return "\t".join(gentilicios)
    

def main():
    pagina = codecs.open("es.wiki", 'r', 'UTF-8').read()

    todos =re.findall(r'{{bandera2.([^}]*)', pagina)

    encontrados = re.findall(r'{{bandera2.([^}]*).*\n.([^\n<]*).*\n....([\w|\s]*).*\n.([^\n<]*).*\n', pagina)

    print "Total:", len(todos)
    print "encontrados:", len(encontrados)
    print "Perdidos:", set(todos) -set([ pais[0] for pais in encontrados])
    gentilicios= []
    for pais,gentilicio_pais,capital,gentilicio_capital in encontrados:
        if gentilicio_pais.strip():
            gentilicios.append((pais.strip(),
                expand(gentilicio_pais.strip())
            ))
        if gentilicio_capital.strip():
            gentilicios.append((capital.strip(),
                expand(gentilicio_capital.strip())
            ))

    output = codecs.open("gentilicios.out", 'w','UTF-8')
    print "gentilicios", len(gentilicios)
    for gentilicio in gentilicios:
        output.write( gentilicio[0]+"\t"+gentilicio[1] + "\n")

if __name__ == "__main__":
    main()

# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


import codecs
import re


def expand(gentilicio):
    gentilicios = []
    gentilicio =  gentilicio.replace(",", "").replace("/", "")
    variantes = gentilicio.split(" o ")
    for variante in variantes :
        generos = variante.split(" ")
        if len(generos) >1:
            generos[1] = generos[1].replace("-", generos[0][:-(len(generos[1])-1)])
        gentilicios.extend(generos)
    return "\t".join(gentilicios)


def main():
    file_name = "files/demonym/es.wiki"
    page = codecs.open(file_name, 'r', 'UTF-8').read()

    all_entries = re.findall(r"{{bandera2.([^}]*)", page)

    found_entries = re.findall(r'{{bandera2.([^}]*).*\n.([^\n<]*).*\n....([\w|\s]*).*\n.([^\n<]*).*\n', page)

    print "All:", len(all_entries)
    print "found:", len(found_entries)
    print "Lost:", set(all_entries) - set([country[0] for country in found_entries])
    demonyms = []
    for country, country_demonym, capital, demonym_capital in found_entries:
        if country_demonym.strip():
            demonyms.append((country.strip(),
                             expand(country_demonym.strip())
            ))
        if demonym_capital.strip():
            demonyms.append((capital.strip(),
                             expand(demonym_capital.strip())
            ))

    output = codecs.open("demonyms.out", 'w', 'UTF-8')
    print "Demonyms: ", len(demonyms)
    for demonym in demonyms:
        output.write( demonym[0]+"\t"+demonym[1] + "\n")


main()

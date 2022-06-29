import csv
from rdflib import Graph,Namespace,RDF,Literal,OWL,URIRef,RDFS
import re

g = Graph()
g.parse("./RDF/enhanced.owl")
uni = Namespace("http://www.csd.uoc.gr/~hy561/2022/1254/2022/5/UniversityOntology#")

progLangs = open("./datasets/CSD-coursesProgrammingLanguage.csv",encoding="utf-8")
progLangs = csv.reader(progLangs,delimiter="\t")

all_langs = set()

for row in progLangs:
    course_uri = uni[row[0]]
    langs = row[1].split(",")
    for lang in langs:
        plang = lang.replace(" ","")
        if plang != "" and plang != "-":
            all_langs.add(plang)
            g.add((course_uri,uni.useLanguage,uni[plang]))

for plang in all_langs:
    g.add((uni[plang],RDF.type,uni.ProgrammingLanguage))
    g.add((uni[plang],uni.name,Literal(plang)))


file = open("./RDF/enhanced.owl","wb")
file.write(g.serialize(format="pretty-xml",encoding="utf-8"))
from rdflib import Graph,Namespace,RDF,Literal,OWL,URIRef,RDFS
import re
import json

g = Graph()
g.parse("./RDF/enhanced.owl")
uni = Namespace("http://www.csd.uoc.gr/~hy561/2022/1254/2022/5/UniversityOntology#")

people = open("./datasets/CSD-people.json",encoding="utf-8")
people = json.load(people)

for person in people:
    person_uri = uni[person["people_name_en"].replace(" ","_")]
    g.add((person_uri,RDF.type,uni.Professor))
    g.add((person_uri,uni.email,Literal(person["people_email"])))
    g.add((person_uri,uni.name,Literal(person["people_name_en"])))
    g.add((person_uri,uni.text,Literal(person["people_text_en"])))
    g.add((person_uri,uni.webpage,Literal(person["people_ext_url"])))
    g.add((person_uri,uni.worksIn,uni.Computer_Science_Department))



file = open("./RDF/enhanced.owl","wb")
file.write(g.serialize(format="pretty-xml",encoding="utf-8"))
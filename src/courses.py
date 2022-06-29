import json
from rdflib import Graph,Namespace,RDF,Literal,OWL,URIRef,RDFS
import re

g = Graph()
g.parse("./Ontology/UniversityOntology.owl")
uni = Namespace("http://www.csd.uoc.gr/~hy561/2022/1254/2022/5/UniversityOntology#")

courses = open("datasets\CSD-courses.json",encoding="utf-8")
courses = json.load(courses)

for course in courses:
    course_code = course["course_code_en"].replace(" ","")
    course_uri = uni[course_code]
    code = re.compile(r"\d+").findall(course_code)
    if len(code) > 0:
        year = code[0][0]
        g.add((course_uri,uni.yearOfStudy,Literal(year)))
        if int(year) <= 4:
            g.add((course_uri,RDF.type,uni.UndergraduateCourse))
        else:
            g.add((course_uri,RDF.type,uni.GraduateCourse))
    else:
        g.add((course_uri,RDF.type,uni.Course))
   
    g.add((course_uri,uni.name,Literal(course["course_name_en"])))
    g.add((course_uri,uni.course_ects,Literal(course["ects"])))
    if course["course_email"] != "":
        g.add((course_uri,uni.email,Literal(course["course_email"])))
    g.add((course_uri,uni.text,Literal(course["course_text_en"])))

    if(course["required_en"] != ""):
        req = re.compile(r"[A-Za-z]+-\d+").findall(course["required_en"])
        sug = re.compile(r"[A-Za-z]+-\d+").findall(course["suggested_en"])
        if len(sug) > 0:
            for s in req:
                g.add((course_uri,uni.recomendedCourse,uni[s])) 
        if len(req) > 0: 
            for r in req:
                g.add((uni[r],uni.isPrerequisiteOf,course_uri)) 

file = open("./RDF/enhanced.owl","wb")
file.write(g.serialize(format="pretty-xml",encoding="utf-8"))
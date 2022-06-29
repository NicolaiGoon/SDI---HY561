import json
from rdflib import Graph,Namespace,RDF,Literal,OWL,URIRef,RDFS
import re
import csv

g = Graph()
g.parse("./RDF/enhanced.owl")
uni = Namespace("http://www.csd.uoc.gr/~hy561/2022/1254/2022/5/UniversityOntology#")

subjects = open("./datasets/subjectsForPerioxiD.txt",encoding="utf-8")
subjects = csv.reader(subjects,delimiter=";")

all_subjects = set()
all_subject_names = {}

for row in subjects:
    course_uri = uni[row[0]]
    code = re.compile(r"\d+").findall(row[0])
    if len(code) > 0:
        year = code[0][0]
        if int(year) <= 4:
            g.add((course_uri,RDF.type,uni.UndergraduateCourse))
        else:
            g.add((course_uri,RDF.type,uni.GraduateCourse))
    else:
        g.add((course_uri,RDF.type,uni.Course))
    subjects_for_course = row[1].split(",")
    for subject in subjects_for_course:
        subject_uri = uni[subject.replace(" ","_")]
        g.add((course_uri,RDF.type,uni.Course))
        g.add((course_uri,uni.relatedSubject,subject_uri))
        g.add((course_uri,uni.inArea,uni.Information_Systems))
        all_subjects.add(subject_uri)
        all_subject_names[subject_uri] = subject.replace(" ","_")

for sub_uri in all_subjects:
    g.add((sub_uri,RDF.type,uni.Subject))
    g.add((sub_uri,uni.name,Literal(all_subject_names[sub_uri])))
    g.add((sub_uri,uni.inArea,uni.Information_Systems))


# add classrooms (dataset is too small)
classrooms = [("Amphitheater_A",120),("Amphitheater_B",174),("A113",77),("A121",56),("A125",59),("H204",59),("H206",26),("H208",26),("E311",24),("E313",48)]

for classroom in classrooms:
    g.add((uni[classroom[0]],RDF.type,uni.Classroom))
    g.add((uni[classroom[0]],uni.capacity,Literal(classroom[1])))
    g.add((uni[classroom[0]],uni.atLocation,uni.Computer_Science_Department))



file = open("./RDF/enhanced.owl","wb")
file.write(g.serialize(format="pretty-xml",encoding="utf-8"))
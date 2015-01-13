#!/usr/bin/env python

''' 
easy_install pip
pip install -r requirements.txt
'''

import yaml
from Cheetah.Template import Template
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDFS

DWC=Namespace("http://rs.tdwg.org/dwc/terms/")
DC=Namespace("http://purl.org/dc/terms/")
DWCA=Namespace("http://rs.tdwg.org/dwc/terms/attributes/")

def buildHtml():
    data=parseTerms()
    print """building html files"""
    html = Template(file="recommended.tmpl", searchList=[data])
    recommended = open("../terms/index.html", "w")
    recommended.write(str(html))
    recommended.close()    

def buildDownloads():
    print """building downloads"""
    print """TBD"""


def veriyfCompleteness(graph, yaml):    
    print """veriyf graph completeness"""
    print """TBD"""

def anchorLinks(x):
    print """TBD"""
    
def getTermDef(name, g):
    t={}
    t["name"]=name
    t["fullname"]="dwc:"+name
    if name.startswith("DC_"):
        name=name[3:]
        uri=DC[name]
        t["name"]="dcterms:"+name
        t["fullname"]=t["name"]
    elif name.find(" ") > 0:
        uri=None
    else:
        uri=DWC[name]
    t["uri"]=uri
    t["label"]=g.value(subject=uri, predicate=RDFS.label)
    t["class"]=g.value(subject=uri, predicate=DWCA.organizedInClass)
    t["definition"]=g.value(subject=uri, predicate=RDFS.comment)
    t["comment"]=g.value(subject=uri, predicate=DC.description)
    t["version"]=g.value(subject=uri, predicate=DC.hasVersion)
    return t
    
def parseTerms():
    with open('term_order.yaml', 'r') as f:
        order = yaml.load(f)
    with open('dc.yaml', 'r') as dcf:
        dc = yaml.load(dcf)
    g = Graph()
    g.parse("../terms/dwc_normative.rdf")
    for t in dc:
        uri=DC[t]
        g.add( (uri, RDFS.comment, Literal(dc[t]["definition"])) )        
        g.add( (uri, DC.description, Literal(dc[t]["comment"])) )        
        g.add( (uri, DC.hasVersion, URIRef(dc[t]["details"])) )
    # before we continue verify we have all terms covered in both the order yaml and the graph
    veriyfCompleteness(g, order)
    data={}
    groups=[]
    for groupData in order:
        group=getTermDef(sorted(groupData.keys())[0], g)
        groups.append(group)
        group["terms"]=[]
        for t in sorted(groupData.values())[0]:
            group["terms"].append(getTermDef(t, g))            
    data["groups"]=groups
    return data



if __name__ == "__main__":
    buildHtml()
    buildDownloads()

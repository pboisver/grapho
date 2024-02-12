from token import NEWLINE

import pytest
from grapho.namespace import AliasingDefinedNamespace
from loguru import logger
from rdflib import FOAF, RDF, Graph, Namespace, URIRef
from rdflib.namespace import NamespaceManager
from rdflib.resource import Resource


EX = Namespace("http://example.org/")


def test_slice():
    g = Graph(bind_namespaces="core")
    g.bind("foaf", FOAF)
    g.bind("ex", EX)

    g.add((EX.bob, RDF.type, FOAF.Person))

    logger.info(g.serialize(format="json-ld", auto_compact=True))

    sliced_g = list(g[:])

    assert "" in sliced_g


graphitti = """
{
    "@context": {
        "ex": "http://example.org/",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "hoppy": "http://rabbits.r.us#"
    },
    "@graph": [
    {
        "@id": "ex:bob",
        "@type": "foaf:Person"
    },
    {
        "@id": "ex:foofoo",
        "@type": "hoppy:rabbit"
    }
    ]
}
"""


_NM = NamespaceManager(Graph(), bind_namespaces="core")
_NM.bind("ex", EX)
_NM.bind("foaf", FOAF)


def test_load_with_parse(capsys):
    g = Graph().parse(data=graphitti, format="json-ld")

    g.namespace_manager.namespaces = _NM.namespaces

    with capsys.disabled():
        print(g.serialize(format="json-ld", auto_compact=True))

    pass

class HOPPY(AliasingDefinedNamespace):
    _NS = Namespace("http://rabbits.r.us#")
    Rabbit: URIRef

    snuggles: URIRef
    munches: URIRef

    carrots: URIRef
    grapes: URIRef
    
_NM.bind("hoppy", HOPPY)


def load_with_blank_nodes(capsys):
    g = Graph().parse(data=graphitti, format="json-ld")
    
    bob = g.resource(EX.bob)
    g.add((EX.ted, RDF.type, FOAF.Person))
    
    foofoo = g.resource(EX.foofoo)
    floppy = g.resource(EX.floppy)
    floppy.add(RDF.type, HOPPY.Rabbit)

    # bob.add(HOPPY.snuggles, EX.foofoo)
    bob[HOPPY.snuggles] = EX.foofoo  # warning: this *replaces* <bob, snuggles, ...>
    bob.add(HOPPY.snuggles, EX.floppy)

    foofoo.add(FOAF.knows, EX.carol)
    foofoo.add(FOAF.knows, EX.ted)
    floppy.add(FOAF.knows, EX.ted)
    floppy.add(FOAF.knows, EX.alice)

    bob_snuggle_bun_frens = set(bob.objects(HOPPY.snuggles / FOAF.knows))
    
    with capsys.disabled(): 
        print("\n------- bob HOPPY.snuggles / FOAF.knows fren ----------")
        for fren in bob_snuggle_bun_frens:
            print(fren.qname())

    g.namespace_manager.namespaces = _NM.namespaces

    with capsys.disabled():
        print("------- g: Graph (format='n3') ----------")
        print(g.serialize())
        print("------- g: Graph (format='json-ld', auto_compact=True) ----------")
        # print(g.serialize(format='json-ld', auto_compact=True))

    pass

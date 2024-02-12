from itertools import count
from grapho.namespace import AliasingDefinedNamespace
from loguru import logger
from rdflib import FOAF, RDF, Graph, Literal, Namespace, URIRef
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

    # assert URIRef('http://example.org/bob') in sliced_g


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


def test_load_with_blank_nodes(capsys):
    g = Graph().parse(data=graphitti, format="json-ld")

    ted = g.resource(EX.ted)
    ted.add(RDF.type, FOAF.Person)
    ted.add(FOAF.name, Literal("Tedward"))

    bob = g.resource(EX.bob)
    bob[HOPPY.snuggles] = EX.foofoo  # warning: this *replaces* <bob, snuggles, ...>
    bob.add(HOPPY.snuggles, EX.floppy)
    bob.add(HOPPY.snuggles, EX.foofoo)

    foofoo = g.resource(EX.foofoo)
    foofoo.add(FOAF.knows, EX.carol)
    foofoo.add(FOAF.knows, EX.ted)

    floppy = g.resource(EX.floppy)
    floppy.add(RDF.type, HOPPY.Rabbit)
    floppy.add(FOAF.knows, EX.ted)
    floppy.add(FOAF.knows, EX.alice)

    assert 4 == len(list(bob[HOPPY.snuggles / FOAF.knows]))
    assert 3 == len(set(bob[HOPPY.snuggles / FOAF.knows]))

    assert ted in set(bob[HOPPY.snuggles / FOAF.knows])
    assert bob not in set(bob[HOPPY.snuggles / FOAF.knows])

    result = set(bob[HOPPY.snuggles / FOAF.knows / (RDF.type | FOAF.name)])
    assert Literal("Tedward") and g.resource(FOAF.Person) in result
    # assert g.resource(FOAF.Person) in result

    with capsys.disabled():
        print("\n------- bob HOPPY.snuggles / FOAF.knows fren ----------")
        for fren in bob[HOPPY.snuggles / FOAF.knows]:
            print(fren.qname())

    g.namespace_manager.namespaces = _NM.namespaces

    with capsys.disabled():
        print("------- g: Graph (format='n3') ----------")
        print(g.serialize())
        print("------- g: Graph (format='json-ld', auto_compact=True) ----------")
        # print(g.serialize(format='json-ld', auto_compact=True))

    pass

from grapho.namespace import AliasingDefinedNamespace
from loguru import logger
from rdflib import FOAF, RDF, BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import NamespaceManager

EX = Namespace("http://example.org/")


def test_slice():
    g = Graph(bind_namespaces="core")
    g.bind("foaf", FOAF)
    g.bind("ex", EX)

    g.add((EX.bob, RDF.type, FOAF.Person))

    logger.info(g.serialize(format="json-ld", auto_compact=True))


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
    """a rabbit"""

    snuggles: URIRef
    munches: URIRef

    carrots: URIRef
    grapes: URIRef
    
class PSDO(AliasingDefinedNamespace):
    _NS = Namespace("http://rabbits.r.us#")
    Rabbit: URIRef

    PSDO_000123: URIRef
    pos_gap: URIRef
    """alias for PSDO_000123"""
    
    _alias = {
        'pos_gap': 'PSDO_000123'
    }
    
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
    bob.add(HOPPY.snuggles, EX.floppy)
    bob.add(HOPPY.snuggles, EX.foofoo)
    # bob[HOPPY.snuggles] = EX.foofoo  # warning: this *replaces* <bob, snuggles, ...>

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

    gap = g.resource(PSDO.pos_gap)
    
    with capsys.disabled():
        print("\n------- bob HOPPY.snuggles / FOAF.knows fren ----------")
        for fren in bob[HOPPY.snuggles / FOAF.knows]:
            print(fren.qname())

    g.namespace_manager.namespaces = _NM.namespaces

    with capsys.disabled():
        print("------- g: Graph (format='n3') ----------")
        print(g.serialize(format="n3", auto_compact=True))
        print("------- g: Graph (format='json-ld', auto_compact=True) ----------")
        # print(g.serialize(format='json-ld', auto_compact=True))

    pass


def test_paths():
    
    bnode: BNode = BNode('foo')
    
    assert URIRef(bnode) == URIRef('foo')
    assert bnode.n3() == '_:foo'
    assert str(bnode) == 'foo'
    assert bnode == BNode("foo")  # value object semantics for ==
    assert bnode is not BNode("foo")  # value object semantics for ==
    assert URIRef('foo') is not URIRef('foo')  # different instances
    assert URIRef(BNode("foo")) == URIRef("foo")    
    assert BNode('foo') == BNode(URIRef('foo'))
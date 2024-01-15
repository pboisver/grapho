from loguru import logger
from rdflib import RDF, Graph, Literal, URIRef
from rdflib import FOAF
from rdflib.namespace import NamespaceManager


def test_load_from_cp():
    
    g = Graph()
    # g.bind("schema", "http://schema.org/", override=True, replace=True)
    assert len(g) == 0
    
    g.parse("tests/social_better.json")
    
    ns = dict(g.namespaces())
    
    print(g.serialize(format="turtle"))
    
    assert len(g) == 21 


def test_compact_graph():
    
    g = Graph(bind_namespaces="core")
    g.bind("foaf", FOAF)
    
    bob = URIRef("bob")
    alice = URIRef("alice")
    g.add((bob, RDF.type, FOAF.Person))
    g.add((bob, FOAF.name, Literal("Bob")))
    g.add((bob, FOAF.knows, alice))
    g.add((alice, FOAF.name, Literal("Alice")))
    
    
    logger.info(g.serialize(format="json-ld",auto_compact=True))
    
    pass

def test_compact_with_blank():
    
    core_g = Graph(bind_namespaces="core")
    core_g.bind("foaf",FOAF)

    # Sadly, parse adds back in all the default "rdflib" namspaces
    g = Graph().parse("./tests/bob_carol_ted_alice.json",format="json-ld",publicID="https://example.com/")
    
    # so we set them back here
    g.namespace_manager.namespaces = core_g.namespaces
 
    logger.info(g.serialize(
        format="json-ld",
        auto_compact=True))
    
    pass

        
        
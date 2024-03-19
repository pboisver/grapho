from typing import NamedTuple
from rdflib import RDF, Graph, IdentifiedNode, BNode, URIRef

from loguru import logger


def test_blank_node_create():
    
    g = Graph()
    
    n: BNode = BNode("ABC123")
    
    assert '_:ABC123' == n.n3()
    assert 'ABC123' == str(n)
    
    g.add((n, RDF.type, URIRef('jttp://foo.bar/baz')))
    
    r = g.resource(n)
    
    assert BNode('ABC123') == r.identifier
    
    assert r.value(RDF.type).identifier == URIRef("jttp://foo.bar/baz")
    
    
from collections import namedtuple

def test_named_tuples():
    
    # Define a named tuple type

    class Point(NamedTuple):
        x: int
        y: int


    # Define a function that returns a named tuple
    def get_point() -> Point:
        # do some calculations
        return Point(3, 4)


    # Call the function and unpack the named tuple
    q = get_point()
    x=3
    
    assert x == 3 and q.y == 4

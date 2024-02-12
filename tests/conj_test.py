import pytest
from grapho.namespace import PSDO, AliasingDefinedNamespace
from loguru import logger
from rdflib import FOAF, RDF, XSD, ConjunctiveGraph, Graph, Literal, Namespace, URIRef
from rdflib.plugins.stores.memory import Memory


def test_load_from_cp():
    g = Graph()
    # g.bind("schema", "http://schema.org/", override=True, replace=True)
    assert len(g) == 0

    g.parse("tests/social_better.json")

    # ns = dict(g.namespaces())

    print(g.serialize(format="turtle"))

    assert len(g) == 21


def test_compact_graph():
    PSDO.foo
    PSDO.bar
    g = Graph(bind_namespaces="core")
    g.bind("foaf", FOAF)

    bob = URIRef("bob")
    alice = URIRef("alice")
    g.add((bob, RDF.type, FOAF.Person))
    g.add((bob, FOAF.name, Literal("Bob")))
    g.add((bob, FOAF.knows, alice))
    g.add((alice, FOAF.name, Literal("Alice")))

    logger.info(g.serialize(format="json-ld", auto_compact=True))

    pass


def test_compact_with_blank():
    core_g = Graph(bind_namespaces="core")
    core_g.bind("foaf", FOAF)

    # Sadly, parse adds back in all the default "rdflib" namspaces
    g = Graph().parse(
        "./tests/bob_carol_ted_alice.json",
        format="json-ld",
        publicID="https://example.com/",
    )

    # so we set them back here
    g.namespace_manager.namespaces = core_g.namespaces

    logger.info(g.serialize(format="json-ld", auto_compact=True))

    pass


def test_pocg():
    """
    An RDFLib ConjunctiveGraph is an (unnamed) aggregation of all the Named Graphs
    within a Store. The :meth:`~rdflib.graph.ConjunctiveGraph.get_context`
    method can be used to get a particular named graph for use, such as to add
    triples to, or the default graph can be used.

    This example shows how to create Named Graphs and work with the
    conjunction (union) of all the graphs.
    """

    LOVE = Namespace("http://love.com#")
    LOVERS = Namespace("http://love.com/lovers/")

    mary = URIRef("http://love.com/lovers/mary")
    john = URIRef("http://love.com/lovers/john")

    cmary = URIRef("http://love.com/lovers/mary")
    cjohn = URIRef("http://love.com/lovers/john")

    store = Memory()

    g = ConjunctiveGraph(store=store)
    g.bind("love", LOVE)
    g.bind("lovers", LOVERS)

    # Add a graph containing Mary's facts to the Conjunctive Graph
    gmary = Graph(store=store, identifier=cmary)
    # Mary's graph only contains the URI of the person she loves, not his cute name
    gmary.add((mary, LOVE.hasName, Literal("Mary")))
    gmary.add((mary, LOVE.loves, john))

    # Add a graph containing John's facts to the Conjunctive Graph
    gjohn = Graph(store=store, identifier=cjohn)
    # John's graph contains his cute name
    gjohn.add((john, LOVE.hasCuteName, Literal("Johnny Boy")))

    # Enumerate contexts
    print("Contexts:")
    for c in g.contexts():
        print(f"-- {c.identifier} ")
    print("===================")
    # Separate graphs
    print("John's Graph:")
    print(gjohn.serialize())
    print("===================")
    print("Mary's Graph:")
    print(gmary.serialize())
    print("===================")

    print("Full Graph")
    print(g.serialize())
    print("===================")

    print("Query the conjunction of all graphs:")
    xx = None
    for x in g[mary : LOVE.loves / LOVE.hasCuteName]:  # type: ignore[misc]
        xx = x
    print("Q: Who does Mary love?")
    print("A: Mary loves {}".format(xx))


def test_alias():
    # assert 'AKA: foo' == PSDO.alias('foo')
    assert PSDO.PSDO_000123 == PSDO.foo
    assert PSDO.PSDO_000123 == PSDO["foo"]

    assert PSDO.PSDO_000124 == PSDO["PSDO_000124"]
    assert PSDO.PSDO_000125 == PSDO.baz
    assert "http://purl.obolibrary.org/obo/foo" in PSDO
    assert "bar" in PSDO
    assert "PSDO_000123" in PSDO

    assert Namespace("http://purl.obolibrary.org/obo/") == PSDO._NS
    assert URIRef("http://purl.obolibrary.org/obo/foo") == PSDO._NS.foo

    with pytest.raises(Exception) as e_info:
        PSDO.missing_term
    assert e_info.type is AttributeError

    PSDO._extras.append("missing_term")
    try:
        PSDO.missing_term
    except AttributeError:
        pytest.fail("Should not raise exception")


class TEST_BOB(AliasingDefinedNamespace):
    _NS = Namespace("http://bob.org/")

    BOB_000123: URIRef
    "alias: foo"
    foo: URIRef
    """alias for BOB_000123"""


def test_more_aliases():
    assert TEST_BOB.BOB_000123.n3() == "<http://bob.org/BOB_000123>"

    assert TEST_BOB.foo.n3() == "<http://bob.org/foo>"

    TEST_BOB._alias["bar"] = "foo"

    assert TEST_BOB.bar.n3() == "<http://bob.org/foo>"

    TEST_BOB.foo

    XSD.string

    pass

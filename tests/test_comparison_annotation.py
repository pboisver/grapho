from typing import Optional

import pytest
from loguru import logger
from rdflib import RDF, BNode, ConjunctiveGraph, Graph, URIRef
from rdflib.plugins.stores.memory import Memory
from rdflib.resource import Resource


@pytest.fixture
def perf_info() -> Graph:
    g = Graph()
    g.add(
        (BNode("PerformanceInformation"), RDF.type, URIRef("performance_information"))
    )
    assert 2 == len(g.all_nodes())
    return g


class Comparison:
    def annotate(self, perf_content) -> Optional[Resource]:
        # TODO document why this method is empty

        r = Graph().resource(BNode("annotation1"))

        r.set(RDF.type, URIRef("comparison"))

        return r


def test_comp_annotation_creates_minimal_subgraph():
    mi = Comparison()
    perf_data = {}
    a_node = BNode("annotation1")  # hard-coded for now

    resource = mi.annotate(perf_data)
    graph = resource.graph
    # logger.info(annotation_graph.serialize(format="json-ld"))

    assert isinstance(resource.graph, Graph)

    assert (a_node, None, None) in resource.graph
    assert graph[a_node]
    # either will assert that triples about 'annotation1' exist in the graph
    # Not sure how to directly test that a 'node' exists since a graph is a collection of triples

    assert URIRef("comparison") in set(graph[a_node : RDF.type])


def test_node_is_aggregation_in_performance_content(perf_info):
    mi = Comparison()
    perf_data = {}

    comparison = mi.annotate(perf_data)

    perf_info.add(
        (
            BNode("PerformanceInformation"),
            URIRef("motivating_information"),
            comparison.identifier,
        )
    )

    perf_info += comparison.graph

    assert 3 == len(perf_info)

    assert (comparison.identifier, RDF.type, URIRef("comparison")) in perf_info


def test_with_cg():
    my_mem_fren = Memory()

    perf_info = ConjunctiveGraph(store=my_mem_fren)

    perf_info.add(
        (
            BNode("PerformanceInformation"),
            URIRef("motivating_information"),
            URIRef("a_comparison"),
        )
    )

    logger.info(perf_info.serialize(format="nquads"))

    gpi = Graph(store=my_mem_fren, identifier="mandalorian")
    gpi.add((BNode("fun"), URIRef("bar"), URIRef("baz")))
    gpi.add((BNode("bob"), URIRef("carol"), URIRef("ted")))

    g = perf_info.serialize(format="nquads")
    logger.info(f"\n{g}")


g1 = """
{
  "@context": {
    "dc11": "http://purl.org/dc/elements/1.1/",
    "ex": "http://example.org/vocab#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "ex:contains": { "@type": "@id"}
  },
  "@graph": [
    {
      "@id": "http://example.org/library",
      "@type": "ex:Library",
      "ex:contains": "http://example.org/library/the-republic"
    },
    {
      "@id": "http://example.org/library/the-republic",
      "@type": "ex:Book",
      "dc11:creator": "Plato",
      "dc11:title": "The Republic",
      "ex:contains": ["http://example.org/library/the-republic#introduction",
      "http://example.org/library/the-republic#Conclusion"]
    },
    {
      "@id": "http://example.org/library/the-republic#introduction",
      "@type": "ex:Chapter",
      "dc11:description": "An introductory chapter on The Republic.",
      "dc11:title": "The Introduction"
    }
  ]
}
"""


def test_type_id():
    hasCar = URIRef("http://pfp.org/hasCar")
    r: Resource = Graph().resource(BNode("Bob"))

    r[RDF.type] = URIRef("http://pfp.org/Recipient")
    r.add(hasCar, URIRef("http://pfp.org/Buick"))
    r.add(hasCar, URIRef("http://pfp.org/Rabbit"))

    # print(r.graph.serialize(format="json-ld", indent=2))

    library = Graph().parse(data=g1, format="json-ld")

    print(library.serialize(format="json-ld", indent=2, auto_compact=True))

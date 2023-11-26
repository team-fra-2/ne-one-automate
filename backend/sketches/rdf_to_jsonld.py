import json

from pyld import jsonld
from rdflib import Graph, plugin
from rdflib.serializer import Serializer


rdf_data: str = """
<http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://onerecord.iata.org/ns/cargo#Piece> .
<http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a> <https://onerecord.iata.org/ns/cargo#coload> "false"^^<http://www.w3.org/2001/XMLSchema#boolean> .
<http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a> <https://onerecord.iata.org/ns/cargo#goodsDescription> "ONE Record Advertisement Materials2"^^<http://www.w3.org/2001/XMLSchema#string> .
"""

# Create a graph and parse the RDF data
g = Graph()
g.parse(data=rdf_data, format="turtle")

# Serialize the graph to JSON-LD
jsonld_data = g.serialize(format="json-ld", indent=4)

# Print the JSON-LD output
# Compact the JSON-LD data
# Serialize the graph to JSON-LD
expanded_jsonld = json.loads(g.serialize(format="json-ld"))

# Compact the JSON-LD data
compacted_jsonld = jsonld.compact(expanded_jsonld, {})


# Print the compacted JSON-LD output
print(json.dumps(compacted_jsonld, indent=4))

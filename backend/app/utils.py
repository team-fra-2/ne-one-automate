import json
import logging
from time import time
from typing import Union
from urllib.parse import urlparse
from uuid import uuid4

from pyld import jsonld
from rdflib import Graph

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_url_components(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme, parsed_url.hostname, parsed_url.port


def resolve_graph(node, expanded):
    """
    Recursively resolves references in a JSON-LD node.
    :param node: The current node to resolve (could be a dict or a list).
    :param expanded: The list of all documents in the expanded JSON-LD.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, dict):
                # If value is a dict, resolve it
                node[key] = resolve_node(value, expanded)
            elif isinstance(value, list):
                # If value is a list, iterate and resolve each item
                node[key] = [resolve_node(item, expanded) for item in value]

    elif isinstance(node, list):
        # If the node itself is a list, resolve each of its items
        return [resolve_node(item, expanded) for item in node]

    return node


def resolve_node(item, expanded):
    """
    Resolves a single node (item) by replacing it with the corresponding document if it's a reference.
    :param item: The node to resolve.
    :param expanded: The list of all documents in the expanded JSON-LD.
    """
    if isinstance(item, dict) and "@id" in item and len(item.items()) == 1:
        # Find the document in expanded that matches the @id of the current item
        for document in expanded:
            if "@id" in document and document["@id"] == item["@id"]:
                return resolve_graph(document, expanded)
    return resolve_graph(item, expanded)


def normalize_action_request(action_request: dict) -> dict:
    """
    Convert an action request to a change request
    """
    g = Graph().parse(data=action_request, format="json-ld")
    expanded_jsonld = g.serialize(format="json-ld")

    compacted = json.loads(expanded_jsonld)
    expanded = jsonld.compact(compacted, ctx={})
    if "@graph" in expanded:
        expanded = expanded["@graph"]
    root = None
    for document in expanded:
        if "@id" in document and ("/action-requests/" in document["@id"]):
            root = document

    return resolve_graph(root, expanded)


def normalize_logistics_object(logistics_object: dict) -> dict:
    """
    Normalize a logistics object
    """
    g = Graph().parse(data=logistics_object, format="json-ld")
    expanded_jsonld = g.serialize(format="json-ld")

    compacted = json.loads(expanded_jsonld)
    expanded = jsonld.compact(compacted, ctx={})
    if "@graph" in expanded:
        expanded = expanded["@graph"]
    root = None
    if isinstance(expanded, dict):
        expanded = [expanded]
    for document in expanded:
        if "@id" in document and "/logistics-objects/" in document["@id"]:
            root = document

    resolved_root = resolve_graph(root, expanded)

    return resolved_root


__all__ = ("get_time", "get_uuid")


def get_time(seconds_precision=True) -> Union[int, float]:
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())

# Imports
import xml.etree.ElementTree as ET
import json
from elasticsearch import Elasticsearch
import time


def get_all_attributes(element, ns):
    """
    Recursively gets all of the child elements of parent element
    :param element: XML element to parse
    :param ns: Namespace to remove from attribute names
    :return: Dictionary of elements spanning from the parent element
    """
    attrs = {}

    for child in element:
        if len(child) > 0:
            attrs[child.tag.replace(ns, "")] = get_all_attributes(child, ns)
        else:
            attrs[child.tag.replace(ns, "")] = None

    return attrs


def get_elem_as_dict(element, attribs, ns):
    """
    Recursively gets all of the attributes in attribs for given element, defaulting to None if not found
    :param element: XML element to parse
    :param attribs: Dictionary of attributes to parse for
    :param: ns: Namespace of the XML data
    :return: Dictionary of attribute value pairs for the given element
    """
    results = {}

    if element is None:
        results = {k.replace(ns, ""): v for k, v in attribs.items()}
        return results

    for k, v in attribs.items():
        if isinstance(v, dict):
            results[k] = get_elem_as_dict(element.find(ns + k), v, ns)
        elif element.find(ns + k) is None:
            results[k] = None
        else:
            results[k] = element.find(ns + k).text

    return results


def get_dict_key_count(d):
    """
    Get the count of elements in a dictionary
    :param d: Dictionary to count elements
    :return: Count of elements
    """
    cnt = 0

    for v in d.values():
        if isinstance(v, dict):
            cnt += get_dict_key_count(v)
        else:
            cnt += 1

    return cnt


def make_elasticsearch_index(docs):
    """
    Connect to an Elasticsearch instance and create a new 'sdnentries' index given a list of documents
    :param docs: A list of documents to fill the index
    :return:
    """

    # Establish an Elasticsearch object
    es = Elasticsearch([{'host': 'elasticsearch'}])

    # Wait 20 seconds for connection
    timeout = time.time() + 20
    while not es.ping():
        if time.time() > timeout:
            raise ValueError("Elasticsearch connection failed!!!")

    # Check if index already exists
    if es.indices.exists(index="sdnentries"):
        es.indices.delete(index='sdnentries', ignore=[400, 404])
        print("'sdnentries' index already exists, deleting to replace...")

    print("Creating Elasticsearch index...")

    # Insert each document into the index
    for i, d in enumerate(docs):
        es.index(index='sdnentries', doc_type='sdnentry', id=i, body=json.dumps(d))

    return es


def main():

    # Read the XML file and find the root node and namespace
    tree = ET.parse('data/sdn.xml')
    root = tree.getroot()
    namespace = root.tag[0:root.tag.index("}") + 1]

    # Get a collection of all of the attributes present in sdnEntry elements
    attributes = {}
    for entry in root.findall(namespace + "sdnEntry"):
        attributes.update(get_all_attributes(entry, namespace))

    # Get a collection of all sdnEntry elements with their attribute values
    documents = []
    for entry in root.findall(namespace + "sdnEntry"):
        documents.append(get_elem_as_dict(entry, attributes, namespace))

    num_attr = get_dict_key_count(attributes)
    print("Parsed XML data and found {0} sdnEntry elements with {1} total attributes".format(len(documents), num_attr))

    # Create the Elasticsearch index
    make_elasticsearch_index(documents)


if __name__ == "__main__":

    main()













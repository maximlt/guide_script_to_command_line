"""Helper script for myscript."""
from lxml import etree


def parse_xml(inputfile):
    """Helper function to parse a XML file."""
    tree = etree.parse(inputfile)
    root = tree.getroot()
    return {child.tag: child.text for child in root.getchildren()}

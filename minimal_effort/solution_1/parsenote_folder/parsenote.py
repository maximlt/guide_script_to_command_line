r"""Tool to parse an xml note and print it in a reable format.

Usage:
- Run `python -m parsenote path\to\inputfile
"""
import sys
from lxml import etree

inputfile = sys.argv[1]
tree = etree.parse(inputfile)
root = tree.getroot()
parsed_xml = {child.tag: child.text for child in root.getchildren()}
print(
    f"Note from {parsed_xml['author']} ({parsed_xml['date']})"
    f"  -->  {parsed_xml['content']}"
)

r"""Simple script that does something with one input file given as an argument.

Usage:
- Run `python -m myscript path\to\inputfile
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

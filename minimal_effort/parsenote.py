r"""Tool to parse an xml note and print it in a reable format.

Usage:
- Set the path of the input file in INPUTFILE
- Run `python myscript.py` from the directory of myscript.py
"""
from lxml import etree

INPUTFILE = r"..\inputdata\inputfile.xml"

tree = etree.parse(INPUTFILE)
root = tree.getroot()
parsed_xml = {child.tag: child.text for child in root.getchildren()}
print(
    f"Note from {parsed_xml['author']} ({parsed_xml['date']})"
    f"  -->  {parsed_xml['content']}"
)

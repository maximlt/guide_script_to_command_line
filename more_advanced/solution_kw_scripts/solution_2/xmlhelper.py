"""Helper script for parsenote.

Author: myname
Changelog:
- 0.0.1: xx/xx/xxxx: initial script
- 0.0.2: xx/xx/xxxx: improved doc
"""
from lxml import etree


def parse_xml(xml_file):
    """Helper function to parse a XML file.

    XML file content:
    <note>
    <author>Bob</author>
    <date>18-08-2019</date>
    <content>Call Bill</content>
    </note>

    >>> parse_xml(file)
    {'author': 'Bob', 'date': '18-08-2019', 'content': 'Call Bill'}
    """
    tree = etree.parse(xml_file)
    root = tree.getroot()
    return {child.tag: child.text for child in root.getchildren()}

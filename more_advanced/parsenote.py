r"""Tool to parse an xml note and print it in a reable format.

Usage:
- Run `python -m myscript someinputfile`
"""
import sys
import xmlhelper

inputfile = sys.argv[1]

parsed_xml = xmlhelper.parse_xml(inputfile)
print(
    f"Note from {parsed_xml['author']} ({parsed_xml['date']})"
    f"  -->  {parsed_xml['content']}"
)

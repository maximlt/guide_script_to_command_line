r"""Simple script that does something with one input file.

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

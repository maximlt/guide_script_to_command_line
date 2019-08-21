"""Tool to parse an xml note and print it in a reable format.

Command line usage:
    - Script executed directly
        python parsenote.py [-h/--help] xml_file
    - Script folder in sys.path
        python -m parsenote [-h/--help] xml_file
    - Package parsenote installed
        parsenote [-h/--help] xml_file

Options:
    -h/--help: Print this doctring and exit
Argument:
    xml_file: path to an xml note file

It can also be imported and reused by another script.
Library usage:
import parsenote; processed_file = parsenote.print_formatted_note(note)

Author: myname
Changelog:
- 0.0.1: xx/xx/xxxx: initial script
- 0.0.2: xx/xx/xxxx: added command line ability
"""
import sys
import xmlhelper


def main(args=None):
    """Used when the script is run directly.

    # args: optional list of command line args -> useful for testing cli()

    Return 1 if an error occured, otherwise 0 or None.
    """
    # Get the command line argument.
    if args is None:
        # sys.argv[0] is discarded because it's the module path.
        args = sys.argv[1:]

    # This script requires only one argument.
    if len(args) != 1:
        print("Use -h/--help for command line help.")
        return 0
    if args[0] in ['-h', '--help']:
        # The help is the module docstring.
        print(__doc__, end=" ")
        return 1
    else:
        input_xml = args[0]

    # Main logic.
    parsed_xml = xmlhelper.parse_xml(input_xml)
    print_formatted_note(parsed_xml)


def print_formatted_note(note):
    """Print a note in a nicely formatted way.

    >>> note = dict(author='Bob', date='18-08-2019', content='Call Bill')
    >>> print_formatted_note(note)
    Note from Bob (18-08-2019)  -->  Call Bill
    """
    print(
        f"Note from {note['author']} ({note['date']})"
        f"  -->  {note['content']}"
    )


# True only when the script is executed directly, not when imported.
if __name__ == "__main__":
    sys.exit(main())

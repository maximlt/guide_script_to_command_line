# Improving the minimal command line tool

## Context

We have:
* A Python script [*parsenote.py*](parsenote.py)
* It has one external dependency (`lxml`)
* It has one local dependency (i.e. `import xmlhelper`)
```python
# parsenote.py
"""Simple script that does something with one input file.

Usage:
- Run `python parsenote.py someinputfile`
- or `python -m parsenote someinputfile` if the current folder is in sys.path
"""
import sys
import xmlhelper

inputfile = sys.argv[1]
parsed_xml = xmlhelper.parse_xml(inputfile)
print(
    f"Note from {parsed_xml['author']} ({parsed_xml['date']})"
    f"  -->  {parsed_xml['content']}"
)
```
```python
# xmlhelper.py
"""Helper script for parsenote."""
from lxml import etree

def parse_xml(inputfile):
    """Helper function to parse a XML file."""
    tree = etree.parse(inputfile)
    root = tree.getroot()
    return {child.tag: child.text for child in root.getchildren()}

```
* We execute it with the command `python parsenote.py someinputfile` or with `python -m parsenote someinputfile` (see [here](../minimal_effort/README.md))
The output we get with the [example input file](../inputdata/inputfile.xml) is `Note from Bob (18-08-2019)  -->  Call Bill`

Both files are saved next to each other:
```
my_python_scripts_folder
│   parsenote.py
|   xmlhelper.py
```

## Problem

While the above script can be used as a command line tool, it has the following weaknesses:
- Documentation:
  - The code is poorly documented
  - The user doesn't have any feedback from the tool
- Code:
  - The code in *parsenote.py* cannot be reused easily
  - There is no validation of the command line argument(s) provided by the user
- Distribution:
  - The solutions introduced in the section [*minimal_effort*]((../minimal_effort/README.md)) are kind of brittle

**Goal: improve the code, its documentation and its distribution with an advanced, but still understandable, solution**

## Solution

### What we've done:

- Distribution:
  - A package is created and made installable
    - *parsenote.py* and *xmlhelper.py* are placed in a subfolder *parsenote*
    - A file *\__init__.py* is created in this folder to make it a package
    - A file *setup.py* is created at the same level of *parsenote* to make it installable
  - The package is installed by running `pip install .` from *parsenote_folder*
- Documentation:
  - Module docstring including now:
    - More detailed command line tool usage
    - Library usage
    - Author name, changelog and version number
  - Better function docstring including a usage example
- Code:
  - Main logic separated in two functions (xmlhelper.parse_xml and print_formatted_note)
  so that they can be easily reused and improved
  - main() function that:
    - Cheks that there is only one input argument provided by the user
    - Prints the help (the module docstring) if the argument is -h or --help (classic way to trigger the help)
    - Contains the main logic
    - Runs only if the script is executed directly
  - The local imports are adapted to the package format

### New directory structure

```
my_python_scripts_folder
└───parsenote_folder
    │   setup.py
    └───parsenote
        │   __init__.py
        │   parsenote.py
        │   xmlhelper.py
```

### Modified [*parsenote.py*](solution/parsenote_folder/parsenote/parsenote.py) and [*xmlhelper.py*](solution/parsenote_folder/parsenote/xmlhelper.py)

```python
# parsenote_folder\parsenote\parsenote.py
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
```

```python
# parsenote_folder\parsenote\xmlhelper.py
"""Helper script for parsenote."""
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
```

### New [*\__init__.py*](solution/parsenote_folder/parsenote/__init__.py) file

This file could actually be empty and the code would still work. However, without much
work, we make the content of the *parsenote* package more discovarable to the user (including ourself in 3 weeks).

```python
# parsenote_folder\parsenote\__init__.py

# Make the modules discovarable when importing the package
# with `import parsenote`
from . import parsenote, xmlhelper
# Add the modules parsenote and xmlhelper to the namespace
# when doing `from parsenote import *`
__all__ = ["parsenote", "xmlhelper"]
```

### New [*setup.py*](solution/parsenote_folder/setup.py) file

The content of *setup.py* could be more minimal, but, the suggested one is
already quite short and pretty straightforward to complete.

Note that there are many ways to indicate *setuptools* how to install our modules,
this is just one simple and apparently often used way.

```python
# parsenote_folder\setup.py
from setuptools import setup

setup(
    name="parsenote",  # package name
    version="0.0.2",  # Keep it manually updated
    description="Tool to parse an xml note and print it in a reable format.",
    install_requires=["lxml"],  # make sure it's installed
    packages=["parsenote"],  # point to the package folder
    entry_points={
        "console_scripts": [
            "parsenote=parsenote.parsenote:main"
            # parsenote is now a command available in the environment
            # where it's installed.
            # it runs the main() function in parsenote.py
        ]
    },
)
```
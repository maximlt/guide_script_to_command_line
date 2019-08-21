* [Improving the minimal command line tool](#improving-the-minimal-command-line-tool)
  * [Context](#context)

# Improving the minimal command line tool

## Context

We have:
* A Python script [*parsenote.py*](parsenote.py)
* It has one external dependency (`lxml`)
* It has one local dependency (i.e. `import xmlhelper`)
```python
# parsenote.py
"""Tool to parse an xml note and print it in a reable format.

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
* We execute it with the command `python parsenote.py someinputfile` or with `python -m parsenote someinputfile` (see [here](../minimal_effort/README.md) how to set this up)
The output we get with the [example input file](../inputdata/inputfile.xml) is `Note from Bob (18-08-2019)  -->  Call Bill`.

Both files are saved next to each other:
```
my_python_scripts_folder
│   parsenote.py
|   xmlhelper.py
```

## Problem

While the above script can be used as a command line tool, it has the following **weaknesses**:
- Documentation:
  - The code is poorly documented
  - The user doesn't have any feedback from the tool
- Code:
  - The code in *parsenote.py* cannot be reused easily
  - There is no validation of the command line argument(s) provided by the user
- Distribution:
  - The solutions introduced in the section [*minimal_effort*]((../minimal_effort/README.md)) are kind of brittle

**Goal: improve the code, its documentation and its distribution with an advanced, but still understandable, solution**

## Suggested solution

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

Changes brought to *parsenote.py* are inspired from Python standard library modules (e.g. see *timeit.py*).

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

Note that there are many alternative ways to indicate *setuptools* how to install our modules,
this is just one simple and apparently often used way (see [here](https://github.com/pypa/sampleproject/blob/master/setup.py) for instance).

The versions of Python and of its external depencendy used when developing the script are
not pinned but defined as the minimal versions to be present/installed.

```python
# parsenote_folder\setup.py
from setuptools import setup

setup(
    name="parsenote",  # package name
    version="0.0.2",  # keep it manually updated
    description="Tool to parse an xml note and print it in a reable format.",
    python_requires=">=3.7",  # make sure the right version of python is used
    install_requires=["lxml>=4.4"],  # make sure it's installed
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

# Alternative ways to distribute the scripts

See the [*distutils doc*](https://docs.python.org/3.7/distutils/examples.html) for more details about how to indicate *setuptools.setup* where to find our two scripts.

## Use *\__main__.py*

We just need to add a file *\__main__.py* in the package folder:

```python
# parsenote\__main__.py
from .parsenote import main
main()
```

Now executing `python -m parsenote someinputfile` runs *\__main__.py* and excute the *main* function.

## Use of the `scripts` keyword in *setup.py*

### Intro

Let's say we have the following *setup.py* file:
```python
from setuptools import setup

setup(
    name="mytool",  # package name
    scripts=["a_python_script.py", "a_batch_script.bat"],
)
```
`scripts=['a_python_script.py', 'a_batch_script.bat']` adds these files to the *Scripts* folder of the activated *conda* environment. In that folder you'll find *pip.exe* for example, so run `where pip` to locate it). Because the *Scripts* folder is in the PATH, these files can be run directly from the command line prompt.

### Solution 1: simple batch file executing Python

```
my_python_scripts_folder
└───parsenote_folder
    │   setup.py
    |   parsenote.bat
    |   parsenote.py
    │   xmlhelper.py
```

```dos
REM parsenote.bat
REM %~dp0: expand to the drive letter and path of that batch file
REM %*: all arguments passed to the batch file
python %~dp0parsenote.py %*
```

```python
# parsenote.py
"""Simple command line script."""
import sys
import xmlhelper  # No relative import

...
...
```

```python
# setup.py
from setuptools import setup

setup(
    name="parsenote",  # package name
    scripts=["parsenote.bat", "parsenote.py", "xmlhelper.py"],
)
```

### Solution 2: `python -x` hack in a batch file

```
my_python_scripts_folder
└───parsenote_folder
    │   setup.py
    |   parsenote.bat
    │   xmlhelper.py
```

*parsenote.bat*
```dos
@echo off & python -x "%~f0" %* & goto :eof
"""Simple command line script.

This hack comes from this SO topic:
https://stackoverflow.com/questions/41918065/python-command-line-x-option

-x option: from the docs (https://docs.python.org/3/using/cmdline.html)
The -x option skips the first line of the source, allowing use of non-Unix
forms of #!cmd. This is intended for a DOS specific hack only.

%~f0: Full name of the currently executing batch file

%*: all arguments passed to the batch file
So it's possible execute: parsenote inputfile

xmlhelper.py can sit next to parsenote.bat because sys.path[0] is the directoyy
of the script invoking the Python interpreter.
See the docs https://docs.python.org/3.7/library/sys.html#sys.path
"""
import sys
import xmlhelper  # No relative import

...
...
```

```python
# setup.py
from setuptools import setup

setup(
    name="parsenote",  # package name
    scripts=["parsenote.bat", "xmlhelper.py"],
)
```

### Solution 3: executable .py files

Disclaimer: I couldn't test that one because my Windows 10 didn't want to associate .py files with the command I defined with *ftype*.

Python files (*.py*) can be directly interpreted when running *myscript.py* from the command prompt if set up properly.
See the [Python docs](https://docs.python.org/3.3/using/windows.html#executing-scripts-without-the-python-launcher) to set Windows.

```
my_python_scripts_folder
└───parsenote_folder
    │   setup.py
    |   parsenote.py
    │   xmlhelper.py
```

```python
# parsenote.py
"""Simple command line script."""
import sys
import xmlhelper  # No relative import

...
...
```

```python
from setuptools import setup

setup(
    name="parsenote",  # package name
    scripts=["parsenote.py", "xmlhelper.py"],
)
```

### Notes

- With those solutions *parsenote* cannot be imported because *\Scripts* isn't in *sys.path*.
- For the solution 1 and 2, `conda activate someenv` (given that *conda* is in the PATH) could be added at the top of each batch file to activate a specific environment (e.g. python 3.6) before running to script. In that case, it's not required to `pip install` the scripts as described above, instead, they should just be placed together somewhere in a folder available in the PATH (e.g. add \mypythonscripts\ to the PATH). Note that `conda activate` is a little slow.
- `pip uninstall parsenote` will remove all the files added to *Scripts*.
- Two references from SO [here](https://stackoverflow.com/questions/23324353/pros-and-cons-of-script-vs-entry-point-in-python-command-line-scripts) and [there](https://stackoverflow.com/questions/45114076/python-setuptools-using-scripts-keyword-in-setup-py).

## Use of `py_modules` keyword in *setup.py*

The keywork argument `py_modules` available to setuptools.setup() seems to be a less used way
to package a project.

```
my_python_scripts_folder
└───parsenote_folder
    │   setup.py
    └───parsenote
        │   parsenote.py
        └───xmlhelper.py
```

```python
# parsenote.py
"""Simple command line script."""
import sys
from . import xmlhelper  # Relative import required

...
...
```

```python
# setup.py
from setuptools import setup

setup(
    name="parsenote",  # package name
    # scripts name given without their .py extension
    # if the scripts and setup.py are within the same folder,
    # the scripts will be installed at the root of *\site-packages\*,
    # let's try to keep things separated.
    py_modules=["parsenote/parsenote", "parsenote/xmlhelper"],
    entry_points={
        "console_scripts": [
            # even if parsenote (the folder) isn't a regular package (no __init__.py)
            # it can be accessed with the dot method because it (probably)
            # is an implicit namespace package (see PEP 420).
            "parsenote=parsenote.parsenote:main"
            # parsenote is now a command available in the environment
            # where it's installed.
            # it runs the main() function in parsenote.py
        ]
    },
)
```

# General Notes

## Going even further

- Git the repo
- Better check the validity of the input argument (is it even an XML file?)
- Add some tests (see *pytest*) and automate the whole thing (see *tox*)
- Publish it to PyPi if it's worth sharing!

## Misc
- Difference between sys.path and PYTHONPATH? From `python --help`:
```
  PYTHONPATH   : ';'-separated list of directories prefixed to the
               default module search path.  The result is sys.path.
```
- *flit* can do pretty much the same install with a simple *myproject.toml* instead of *setup.py*, but as of today (08/2019), `flit install -s` or `flit install --pth-file` seems to break `conda list` on Windows :(
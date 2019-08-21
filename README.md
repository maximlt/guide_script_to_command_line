# WIP - Turn a simple Python script into command line tool made available in a conda environment

## Intro

This repo contains examples and explanations about **how to turn a simple Python script into a command line script/tool**. While this may seem like a trivial task for seasoned developers, this isn't actually easy for beginners or occasional users of Python. The benefits of learning how to make that conversion can be huge though, making availabe (i.e. from the command line prompt) any custom script, ready to fire!

We use an examplary script that parses one XML input file whose path is hard-coded and prints some output. It is demonstrated that building a command line script from that initial script can be achieved with minimal effort. But it is also demonstrated that with some additional but limited work, it is possible to get a quite advanced and robust tool.

## General setup

While the Zen of Python stipulates that `There should be one-- and preferably only one --obvious way to do it`, it is difficult for beginners/non-developers to come up with an **obvious** way to create that command line script. It is thus interesting to constrain the problem space to come up with a reduced set of solutions. The solutions suggested in this repo work for the following general setup:
- Windows 10
- conda 4.7.11 (installed from an Anaconda distribution and updated afterwards)
- python 3.7.3
- pip 19.2.2

It is likely that the solutions would work for a different setup (e.g. Windows 7, different versions of conda/pip/python), however, they haven't been tested so you're on your own unfortunately.


## For a standalone script: two solutions with minimal effort

[Here](minimal_effort/README.md) you'll find two simple solutions for creating a command line script from a standalone script.

The first one requires to create a *setup.py* file and to run `pip install -e .` , the second one requires to manually add a *path configuration file* (.pth) to *Lib\site-packages*.

Note that both solutions work well with a script that relies on other/helper scripts located in the same directory.

[Solution with minimal effort](minimal_effort/README.md#from-a-standalone-script-to-a-command-line-tool-with-minimal-effort)
* [Context](minimal_effort/README.md#context)
* [Read one command line argument](minimal_effort/README.md#read-one-command-line-argument)
* [Solution 1: *pip install -e .*](minimal_effort/README.md#solution-1-pip-install--e-)
* [Solution 2: add a *path configuration file*](minimal_effort/README.md#solution-2-add-a-path-configuration-file)
* [Pros and cons](minimal_effort/README.md#pros-and-cons)

## A slightly more advanced case with a script supported by another local script

[Here](more_advanced/README.md) you'll a solution for creating a command line script from a script that makes use of another local script (`import somehelperscript`). This solution is slightly more advanced compared to the previous two solutions because we improve the code, its documentation and the way it is distributed. While these small changes are limited compared to what experienced developers could do (TODO: add ref), they make our script more understandable, robust and reusable.

[More Advanced Case](more_advanced/README.md)
* [Improving the minimal command line tool](more_advanced/README.md#improving-the-minimal-command-line-tool)
  * [Context](more_advanced/README.md#context)
  * [Problem](more_advanced/README.md#problem)
  * [Suggested solution](more_advanced/README.md#suggested-solution)
    * [What we've done](more_advanced/README.md#what-weve-done)
    * [New directory structure](more_advanced/README.md#new-directory-structure)
    * [Modified *parsenote.py* and *xmlhelper.py*](more_advanced/README.md#modified-parsenotepy-and-xmlhelperpy)
    * [New *\__init__.py* file](more_advanced/README.md#new-_init_py-file)
    * [New *setup.py* file](more_advanced/README.md#new-setuppy-file)

[Alternative ways to distribute the scripts](more_advanced/README.md#alternative-ways-to-distribute-the-scripts) are also introduced:
  * [Use *\__main__.py*](more_advanced/README.md#use-_main_py)
  * [Use of the `scripts` keyword in *setup.py*](more_advanced/README.md#use-of-the-scripts-keyword-in-setuppy)
    * [Solution 1: simple batch file executing Python](more_advanced/README.md#solution-1-simple-batch-file-executing-python)
    * [Solution 2: `python -x` hack in a batch file](more_advanced/README.md#solution-2-python--x-hack-in-a-batch-file)
    * [Solution 3: executable .py files](more_advanced/README.md#solution-3-executable-py-files)
  * [Use of `py_modules` keyword in *setup.py*](more_advanced/README.md#use-of-py_modules-keyword-in-setuppy)
  * [Going even further](more_advanced/README.md#going-even-further)

## Summary

### The original script :japanese_ogre:...

```python
r"""Tool to parse an xml note and print it in a reable format.

Usage:
- Set the path of the input file in INPUTFILE
- Run `python parsenote.py` from the directory of parsenote.py
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
```

We usually execute it with the command `python parsenote.py`
The output we get with the [example input file](inputdata/inputfile.xml) is:
```
Note from Bob (18-08-2019)  -->  Call Bill
```

## ...turned into a command line script :wrench: ...

```python
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

```

## ...made distributable with a *setup.py* file saved in the same directory :two_men_holding_hands: ...

```python
# setup.py
from setuptools import setup

setup(
    name="parsenote-editable",
    install_requires=["lxml"],
)
```

## ...and a quick way to install it :motorcycle: ...

- Open the Anaconda command prompt and activate the targeted environment with `conda activate envname` (not required if that environment is in the PATH, as it can be for *base* if adding *conda* to PATH was selected during the Anaconda install).
- `cd path\to\parsenote_folder`
- Execute `pip install -e .` to install the script in editable/develop mode. In this way, changes to *parsenote.py* will be directely reflected so there is no need to `pip install` it again.

## ...so that it can be used super easily :clap: !

- Open the Anaconda command prompt and activate the environment where *parsenote* is installed (not required if that environment is in the PATH, as it can be for *base* if adding *conda* to PATH was selected during the Anaconda install)
- Execute `python -m parsenote someinputfile`

## But we can go just a little further to improve it :100: ...

### ...by separating the code into two scripts :family: ...

```python
# parsenote_folder\parsenote\xmlhelper.py
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
```
### ...refactoring and documenting the main code :book: ...

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
from . import xmlhelper


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

### ...turning it into a package :package: ...

```python
# parsenote_folder\parsenote\__init__.py

# Make the modules discovarable when importing the package
# with `import parsenote`
from . import parsenote, xmlhelper
# Add the modules parsenote and xmlhelper to the namespace
# when doing `from parsenote import *`
__all__ = ["parsenote", "xmlhelper"]
```

### ...distributing it properly :mailbox_with_mail: ...

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

## ...and be proud of ourself :muscle: !

Now our code is:
- better documented
- easier to reuse both as a command line tool (better interactive doc) and a library (it can be imported)
- easier to distribute (we're not far from being able to upload it on PyPi!)

## But! There's still a long way to go :running: ...

We could add:
- some sort of input data validation
- tests
- and millions of other things to make it an advanced package

If this piece of code isn't something too serious (let's say we use it instead of firing Excel and doing some horrible things manually), this is already a great job!

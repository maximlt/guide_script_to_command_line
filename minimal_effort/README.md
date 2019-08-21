# From a standalone script to a command line tool with minimal effort

## Context

We have:
* A single Python script [*parsenote.py*](parsenote.py) parameterized with one hard-coded input path
* It has no local dependencies (i.e. **no** `import myotherscript`)
* It has one external dependency (`lxml`, but note that this isn't very important, it could either lots of them of none of them)
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
* We usually execute it with the command `python parsenote.py`
The output we get with the [example input file](../inputdata/inputfile.xml) is:
```
Note from Bob (18-08-2019)  -->  Call Bill
```

It's saved in a convenient location:
```
my_python_scripts_folder
│   parsenote.py
```

**Goal: turn this script with minimal effort into a command line tool that accepts the input file path as an argument.**

Notes:
- Before running `python parsenote.py`, we may have to activate a *conda* environment (`conda activate myenv`) or have Python available globally, if we chose to add *Anaconda/Miniconda* to the PATH during the install process or afterwards (see this [SO](https://stackoverflow.com/questions/44597662/conda-command-is-not-recognized-on-windows-10) question for instance).

## Read one command line argument

First, it's required to remove the hard-coded part of the script and change it to read the command line argument (here, an input file path) it's going to be called with. Note that just a couple of changes were required.
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
### Notes:
- `sys` is a built-in module. `sys.argv` is the list of command line arguments passed to a Python script. `sys.argv[0]` is the script name (see the [Python docs](https://docs.python.org/3/library/sys.html#sys.argv)).

## Solution 1: *pip install -e .*

The `-e` (same as `--editable`) switch of `pip install` [installs  a project in editable mode (i.e. setuptools “develop mode”) from a local project path](https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-e). The dot at the end (`.`) just points to the current directory.

Installing a project in *editable* mode means that changes *parsenote.py* (not *setup.py*!) are reflected when we run the installed project.

The trick here is that **we're interested in a side effect** of `pip install -e .`: it adds the current folder to [*sys.path*](https://docs.python.org/3/library/sys.html#sys.path) (a list of strings that specifies the search path for modules). In practice, it adds this folder to a [path configuration file](https://docs.python.org/3.7/library/site.html) named *easy_install.pth* and saved in *Lib\site-packages* (run this command to find *site-packages*: `python -c "import site; print(site.getsitepackages())"`). Now if you run `python -c "import sys; print(sys.path)"` you'll see that our project folder is included in the list of paths.

Why is this interesting? Because now *parsenote.py* can be executed with the simple command `python -m parsenote someinputfile` **from any directory**. We've made *parsenote.py* globally available for Python. Running Python with the `-m` flag [searches *sys.path* for the named module and execute its contents as the __main__ module](https://docs.python.org/3.7/using/cmdline.html#cmdoption-m).

So we need to create a [*setup.py*](solution_1/parsenote_folder/setup.py) file to indicate *pip* how to install our project. As this whole thing is just a workaround to add our project folder to *sys.path*, we can have a pretty minimal *setup.py*:
```python
from setuptools import setup

setup(
    name="parsenote-editable",
    install_requires=["lxml"],
)
```
The `name` keyword isn't important here because we'll always run *parsenote.py* with `python -m parsenote someinputfile`. It's just useful to see what project/folder we've installed when executing `conda list` or `pip list`. Or to uninstall the project with `pip uninstall parsenote-editable`. Tring to `import parsenote-editable` will raise a `ModuleNotFoundError` because `parsenote-editable` isn't a package. It's possible to `import parsenote` but that will also raise an error because *parsenote.py* isn't really importable (it's a command line script now after all).

We've added the `install_requires` keyword just to make sure that the external dependency of *parsenote.py* is installed in our conda environment.


*setup.py* needs to be saved next to *parsenote.py*, here is simple and convenient directory structure:
```
my_python_scripts_folder
└───parsenote_folder
    │   parsenote.py
    │   setup.py
```
Given the above directory structure, just run `pip install -e .` from *parsenote_folder*.

### Notes
- Executing `pip install .` instead of `pip install -e .`  will install *parsenote-editable* as defined in *setup.py*, so, it's going to be an "empty" install as no package/module/script is defined in *setup.py*. `python -m parsenote someinputfile` will thus fail.
- It is actually possible to install a "package" in development mode with a *setup.py* file as simple as `from setuptools import setup; setup()`. However, that breaks `conda list`. `pip list` doesn't break but displays the package with the name *UNKNOWN*, to remove the package execute `pip uninstall UNKNOWN` (that is weird).
- Some more info about [*site-packages*](https://stackoverflow.com/questions/31384639/what-is-pythons-site-packages-directory) from SO.
- Running `pip install -e .` creates a file *parsenote_editable.egg-link* in *site-packages* ([egg-link doc from setuptools](https://setuptools.readthedocs.io/en/latest/formats.html#egg-links)). This file contains the path of the folder where *setup.py* lies (same as in *easy-install.pth*). In that folder, a folder *parsenote_editable.egg-info* is created, it contains the project’s metadata ([more info](https://setuptools.readthedocs.io/en/latest/formats.html#eggs-and-their-formats)). In our case, it doesn't contain much as our project is really minimal. But if we were to change *setup.py*, we'd have to run `pip install -e .` gain to reflect those changes.

## Solution 2: add a *path configuration file*

This solution, similar to `solution 1`, is even more straigthforward. **We just add a path configuration file *mypythonscripts.pth* including *parsenote.py*'s folder at the root of *site-packages*.**

Here is a suggested directory structure for that solution:
```
my_python_scripts_folder
└───parsenote_folder
    │   parsenote.py
```

[*mypythonscripts.pth*](solution_2/mypythonscripts.pth) is added at the root of *site-packages*:
```
site-packages
│   mypythonscripts.pth
│   ...
└───lxml
│   │   ...
```
*mypythonscripts.pth* contains:
```
someprefix\my_python_scripts_folder\parsenote_folder
```

Now the path to *parsenote_folder* is automatically added to *sys.path*, and *parsenote.py* can be run with `python -m parsenote someinputfile`.

### Notes:
- Let's assume we have another script we want to turn into a command line tool. It's saved in *myotherscript_folder". Just add the path to this folder on a new line in *mypythonscripts.pth* to make it available (`python -m myotherscript someargs`).
- Similarly to **Solution 1**, changes brought to *parsenote.py* are going to be reflected.

## Pros and cons

**Solution 1**:
- Pros:
  - Runnning `conda list` or `pip list` displays what we "installed"
  - It's possible to add some metadata (e.g. version) to the file *setup.py*
  - The keyword `install_requires` in *setup.py* makes sure the required external dependencies are installed
  - It's closer to being a *package* than with **Solution 2**
- Cons:
  - *pip* is now a requirement
  - There's a bit more work to do

**Solution 2**:
- Pros:
  - It's really straigthforward (just one simple file to create)
- Cons:
  - We have to manually add a path configuration file in Python's directory structure (potential for creating a huge mess there)
  - It's easy to forget what *mypythoncripts.pth* contains
  - The path in *mypythonscripts.pth* isn't synchronized at all with the path of *parsenote.py*, while *pip* in **Solution 1** ensures a (somewhat loose) link


## Additional notes

- In both solutions the path of the project folder is appended to *sys.path*. If *parsenote* (the name) is already used by another module found in the first paths of *sys.path*, `python -m parsenote` will execute that module instead of ours.
- Info about path configuration files found in the Python module *site.py*:
```
A path configuration file is a file whose name has the form
<package>.pth; its contents are additional directories (one per line)
to be added to sys.path.  Non-existing directories (or
non-directories) are never added to sys.path; no directory is added to
sys.path more than once.  Blank lines and lines beginning with
'#' are skipped. Lines starting with 'import' are executed.
```
- If the script relies on one or more helper scripts located in the same directory, both solutions work without any change. Here is an example with a single helper script for *parsenote.py*
```python
# xmlparser.py
"""Helper script for parsenote."""
from lxml import etree


def parse_xml(inputfile):
    """Helper function to parse a XML file."""
    tree = etree.parse(inputfile)
    root = tree.getroot()
    return {child.tag: child.text for child in root.getchildren()}
```
```python
# parsenote.py
"""Tool to parse an xml note and print it in a reable format.

Usage:
- Run `python -m parsenote someinputfile`
"""
import sys
import xmlparser

inputfile = sys.argv[1]

parsed_xml = xmlparser.parse_xml(inputfile)
print(
    f"Note from {parsed_xml['author']} ({parsed_xml['date']})"
    f"  -->  {parsed_xml['content']}"
)
```

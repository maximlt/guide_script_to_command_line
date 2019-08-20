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

  * [Minimal Effort](minimal_effort/README.md)
    * [Context](minimal_effort/README.md##context)
    * [Read one command line argument](minimal_effort/README.md##read-one-command-line-argument)
    * [Solution 1: *pip install -e .*](minimal_effort/README.md##solution-1-pip-install-e)
    * [Solution 2: add a *path configuration file*](minimal_effort/README.md##solution-2-add-a-path-configuration-file)
    * [Pros and Cons](minimal_effort/README.md##pros_and_cons)
    * [## Additional notes](minimal_effort/README.md##additional-notes)

## A slightly more advanced case with a script supported by another local script

[Here](more_advanced/README.md) you'll a solution for creating a command line script from a script that makes use of another local script (in practice, it does `import somehelperscript`). This solution is slightly more advanced than the previous two solutions we improve the code, its documentation and the way it is distributed. While these small changes are limited compared to what experienced developers could do (TODO: ref), they make our script more understanble, robust and reusable.

  * [More Advanced Case](more_advanced/README.md)
    * [Context](more_advanced/README.md##context)
    * [Problem](more_advanced/README.md##problem)
    * [Solution](more_advanced/README.md##solution)

[the `scripts` keyword](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-scripts-keyword-argument)

[example with `py_modules`](https://docs.python.org/3/distutils/introduction.html#a-simple-example)

[minimal directory structure](https://stackoverflow.com/questions/28444747/whats-the-minimal-directory-structure-to-make-setuptools-work-with-one-file-py)

## TODO
  - What if I add myscript.py to The PATH? Can Python find it?
  - List at the end all the different ways to install it (easily): entry_points, py_modules, scripts, PYTHONPATH, .pth in site-packages (https://stackoverflow.com/questions/12257747/permanently-adding-a-file-path-to-sys-path-in-python, although there's an ongoing discussion about them here https://bugs.python.org/issue33944)
  - Switch from `scripts` to `entry_points` in *setup.py* because the former seems not to be used so much and it's not clear what it does exactly (https://stackoverflow.com/questions/45114076/python-setuptools-using-scripts-keyword-in-setup-py) and the latter is the recommended way (https://github.com/pypa/sampleproject/blob/master/setup.py, https://stackoverflow.com/questions/23324353/pros-and-cons-of-script-vs-entry-point-in-python-command-line-scripts)
  - Check how to exit the CLI: return or import sys; sys.exit() ? Or maybe sys.exit(cli()) (See CPython:timeit.py for a great example or https://stackoverflow.com/questions/5280203/what-does-this-mean-exit-main, and look for what cli() should return between 0, 1, 2, etc.)
  - Check whether installing the dependency this way works (starts from a fresh environment)
  - Alternative to consider: (1) add the file folder path to the PATH, (2) execute `python myscript.py` or `python myscript` if *myscript* is a folder containing *\__main__.py* and *some_other_file.py*?
  - Add more info about the general setup? (conda? windows?)

  - Difference between sys.path and PYTHONPATH? From `python --help`:
```
  PYTHONPATH   : ';'-separated list of directories prefixed to the
               default module search path.  The result is sys.path.
```





## Notes:
* pip install -e . based on a setup.py with scripts=['myscript.py'] adds the folder where setup.py is saved to sys.path (!!! If myscript.py next to setup.py, e.g. at src/myscript.py, it's not going to work) and adds an .egg-link file in site-packages containing
```
D:\GoogleDrive\Code\simplescript\setup_scripts\transformed
.
```
It also adds a folder myscript.egg-info next to setup.py
Run it from anywhere with:
`python -m myscript inputfile.txt`
It can be uninstalled with pip uninstall myscript.
Other modules, as long as they're sitting next to setup.py and myscript.py, can be imported from myscript.py.



## Your original script :japanese_ogre:...

```python
"""Simple script that does something with one input file.

Usage:
- Set the path of the input file in INPUTFILE
- Run `python path\to\myscript.py`
"""
import numpy as np

INPUTFILE = "path\to\input.file"

# Read the inputfile, process it and generate some output
...
...
...
```

## ...turned into a command line script :wrench: ...

```python
"""Simple command line script that does something with one input file.

Usage: myscript input.file
"""
import numpy as np

def cli():
    """Wrap all the logic in one function."""
    # This script requires only one argument.
    if len(sys.argv) != 2:
        # Print the help which is the module docstring.
        print("Usage: myscript input.file")
        return  # or sys.exit()?

    # Get the input file path
    inputfile = sys.argv[1]
    # Read the inputfile, process it and generate some output
    ...
    ...
    ...
```

## ...made packageable with a *setup.py* file saved in the same directory :two_men_holding_hands: ...
TODO: check if I need to add an \_\_init__.py
```python
from setuptools import setup

setup(
    name="myscript",
    install_requires=["numpy"],
    entry_points={
        "console_scripts": ["myscript=myscript:cli"]
    },
)
```

## ...and a quick way to install it :motorcycle: ...

- Open the Anaconda command prompt and activate the targeted environment with `conda activate envname` (not required if that environment is in the PATH, as it can be for *base* if adding *conda* to PATH was selected during the Anaconda install)
- `cd path\to\myscriptdirectory`
- Execute `pip install -e .` to install the script in editable/develop mode. In this way, changes to *myscript.py* will be directely reflected so there is no need to `pip install` it again

## ...so that it can be used super easily :clap: !
- Open the Anaconda command prompt and activate the environment where *myscript* is installed (not required if that environment is in the PATH, as it can be for *base* if adding *conda* to PATH was selected during the Anaconda install)
- Execute `python -m myscript someinput.file`

## But we can go just a little further to improve it :100: ...

```python
"""Simple command line script that does something with one input file.

Command line usage: python -m myscript input.file

It can also be imported from another script.
Example: import myscript; processed_file = myscript.process_file(some.file)

Author: myname
Changelog:
- 0.1: xx/xx/xxxx: initial script
- 0.2: xx/xx/xxxx: changed this because of that
"""

import pathlib
import numpy as np

def cli(args=None):
    """Wrap all the logic in one function.

    # args: optional list of command line args -> useful for testing cli()
    """
    # Get the command line argument.
    if args is None:
        args = sys.argv[1:]  # sys.argv[0] is excluded because it's TODO: what?.

    # This script requires only one argument.
    if len(args) != 1:
        # Print the help which is the module docstring.
        print(__doc__, end=" ")
        return  # or sys.exit()?

    # Do something with the input file.
    inputfile = pathlib.Path(args[0])
    processed_data = process_file(inputfile)
    generate_output(processed_file)

def process_file(file):
    """Read a .xxx file, do something and return the processed data as type xx."""
    ...
    return processed_data

def generate_output(data):
    """Generate output (file, stdout, etc.) given some data of type xx."""
    ...

if __name__ == "__main__":
    cli()
```

## ...and be proud of ourself :muscle: !

We took advantage of turning the script into a command line tool for improving, completing and refactoring the code:
- Useful **docstrings** were added to document the code and indicate future users (including ourself!) how to run it
- Functions were created and the classic `if __name__ == "__main__":` was added so that the script can be imported (for instance from a script located in the same repo) without any code running during the import
- The logic was divided into two functions, this creates an interface and makes the code more reusable: someone can only import the first function to write another script. It's also now easier to add more functionalities.

## Notes
- TODO: Descripts scripts rather than entry_points (It is certainly possible to add an **entry_point** to *setup.py* in order to execute directly `myscript someinput.file` but that's already simply enough)
- `scripts=['a_python_script.py', 'a_batch_script.bat']` adds these files to the *Scripts* folder of the activated *conda* environment. If one of these files is Python script, then it's required to configure Windows so that Python files are automatically executed. That can be achieved easily: select *python.exe* as the default program to run *\*.py* files (*pythonw.exe* is more for GUI programs). Then just run `a_python_script` from the command line in the activated environment.
- **flit** can do pretty much the same install with a simple *myproject.toml* instead of *setup.py*, but as of today (08/2019), `flit install -s` or `flit install --pth-file` seems to break `conda list` on Windows
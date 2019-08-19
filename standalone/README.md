# From a standalone script to a command line tool with minimal effort

## The situation

We have:
* A single Python script *myscript.py* including one hard-coded input path
* It has no local dependencies (i.e. no `import myotherscript`)
* But it may have some external dependencies (i.e. `import lxml`)
* We usually execute it with the command `python myscript.py`

It's saved in a convenient location:
```
my_python_scripts_folder
│   myscript.py
```

**Our goal: With minimal effort, turn this script into a command line tool that accepts one argument.**

Notes:
- Before running `python myscript.py`, we may have to activate a *conda* environment (`conda activate myenv`) or have Python available globally, if we chose to add *Anaconda/Miniconda* to the PATH during the install process or afterwards (see this [SO](https://stackoverflow.com/questions/44597662/conda-command-is-not-recognized-on-windows-10) question for instance).

## Reading one command line argument

First, it's required to remove the hard-coded part of the script and change it to read the command line argument (here, an input file path) it's going to be called with.
```python
import sys
inputfile = sys.argv[1]
```
### Notes:
- `sys` is a built-in module.
- `sys.argv` is the list of command line arguments passed to a Python script. `sys.argv[0]` is the script name (see the [Python docs](https://docs.python.org/3/library/sys.html#sys.argv)).

## Solution 1: *pip install -e .*

The `-e` (same as `--editable`) switch of `pip install` [installs  a project in editable mode (i.e. setuptools “develop mode”) from a local project path](https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-e). The dot at the end (`.`) just points to the current directory.

Installing a project in *editable* mode means that changes *myscript.py* (not *setup.py*!) are reflected when we run the installed project.

The trick here is that **we're interested in a side effect** of `pip install -e .`: it adds the current folder to [*sys.path*](https://docs.python.org/3/library/sys.html#sys.path) (a list of strings that specifies the search path for modules). In practice, it adds this folder to a [path configuration file](https://docs.python.org/3.7/library/site.html) named *easy_install.pth* and saved in *Lib\site-packages* (run this command to find *site-packages*: `python -c "import site; print(site.getsitepackages())"`). Now if you run `python -c "import sys; print(sys.path)"` you'll see that our project folder is included in the list of paths.

Why is this interesting? Because now *myscript.py* can be executed with the simple command `python -m myscript someinputfile` **from any directory**. We've made *myscript.py* globally available for Python. Running Python with the `-m` flag [searches *sys.path* for the named module and execute its contents as the __main__ module](https://docs.python.org/3.7/using/cmdline.html#cmdoption-m).

So we need to create a *setup.py* file to indicate *pip* how to install our project. As this whole thing is just a workaround to add our project folder to *sys.path*, we can have a pretty minimal *setup.py*:
```python
from setuptools import setup

setup(
    name="myscript_editable",
    install_requires=["lxml"],
)
```
The `name` keyword isn't important here because we'll always run *myscript.py* with `python -m myscript someinputfile`. It's just useful to see what project/folder we've installed when executing `conda list` or `pip list`. Or to uninstall the project with `pip uninstall myscript_editable`. Tring to `import myscript_editable` will raise a `ModuleNotFoundError` because `myscript_editable` isn't a package. It's possible to `import myscript` but that will also raise an error because *myscript.py* isn't really importable (it's a command line script now after all).

We've added the `install_requires` keyword just to make sure that the external dependency of *myscript.py* is installed in our conda environment.


*setup.py* needs to be saved next to *myscript.py*, here is simple and convenient directory structure:
```
my_python_scripts_folder
└───myscript_folder
    │   myscript.py
    │   setup.py
```
Given the above directory structure, just run `pip install -e .` from *myscript_folder*.

### Notes
- It is actually possible to install a "package" in development mode with a *setup.py* as simple as `from setuptools import setup; setup()`. However, that breaks `conda list`. `pip list` doesn't break but displays the package with the name *UNKNOWN*, to remove the package execute `pip uninstall UNKNOWN` (but that which feels weird).
- Some more info about [*site-packages*](https://stackoverflow.com/questions/31384639/what-is-pythons-site-packages-directory) from SO.
- Running `pip install -e .` creates a file *myscript_editable.egg-link* in *site-packages* ([egg-link doc from setuptools](https://setuptools.readthedocs.io/en/latest/formats.html#egg-links)). This file contains the path of the folder where *setup.py* lies (same as in *easy-install.pth*). In that folder, a folder *myscript_editable.egg-info* is created, it contains the project’s metadata ([more info](https://setuptools.readthedocs.io/en/latest/formats.html#eggs-and-their-formats)). In our case, it doesn't contain much as our project is really minimal. But if we were to change *setup.py*, we'd have to run `pip install -e .` gain to reflect those changes.

## Solution 2: add a path configuration file

This solution, similar to `solution 1`, is even more straigthforward. **We just add a path configuration file *mypythonscripts.pth* including *myscript.py*'s folder at the root of *site-packages*.**

Here is a suggested directory structure for that solution:
```
my_python_scripts_folder
└───myscript_folder
    │   myscript.py
```

*mypythonscripts.pth* is added at the root of *site-packages*:
```
site-packages
│   mypythonscripts.pth
│   ...
└───lxml
│   │   ...
```
*mypythonscripts.pth* contains:
```
someprefix\...\my_python_scripts_folder\myscript_folder
```

Now the path to *myscript_folder* is automatically added to *sys.path*, and *myscript.py* can be run with `python -m myscript someinputfile`.

### Notes:
- Let's assume we have another script we want to turn into a command line tool. It's saved in *myotherscript_folder". Just add the path to this folder on a new line in *mypythonscripts.pth* to make it available (`python -m myotherscript someargs`).
- Changes brought to *myscript.py* are also going to be reflected.

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
  - We have to manually add a path configuration file in Python's directory structure (potential for creating a big mess)
  - It's easy to forget what *mypythoncripts.pth* contains
  - The path in *mypythonscripts.pth* isn't synchronized at all with the path of *myscript.py*, while *pip* in **Solution 1** ensures a loose link


## General notes

- In both solutions the path of the project folder is appended to *sys.path*. If *myscript* (the name of your script) is already used by another module found in the first paths of *sys.path*, `python -m myscript` will execute that module instead of ours.


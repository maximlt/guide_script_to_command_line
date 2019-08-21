# Make the modules discovarable when importing the package
# with `import parsenote`
from . import parsenote, xmlhelper
# Add the modules parsenote and xmlhelper to the namespace
# when doing `from parsenote import *`
__all__ = ["parsenote", "xmlhelper"]

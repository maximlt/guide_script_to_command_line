from setuptools import setup

setup(
    name="parsenote",  # package name
    py_modules=["parsenote/parsenote", "parsenote/xmlhelper"],
    entry_points={
        "console_scripts": [
            "parsenote=parsenote.parsenote:main"
            # parsenote is now a command available in the environment
            # where it's installed.
            # it runs the main() function in parsenote.py
        ]
    },
)

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

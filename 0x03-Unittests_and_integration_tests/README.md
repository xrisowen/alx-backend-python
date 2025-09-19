Python GitHub Client
This project is a small Python client for interacting with the GitHub API to retrieve information about organizations and their repositories. It focuses on using best practices like memoization for efficiency, proper documentation, and type annotations for code quality.

Requirements
Environment: Ubuntu 18.04 LTS, Python 3.7

Style: pycodestyle (version 2.5)

Documentation: All modules, classes, and functions must have comprehensive docstrings.

Type Hinting: All functions and coroutines must be type-annotated.

File Structure: All files must start with #!/usr/bin/env python3 and end with a new line. The README.md file is mandatory.

Files
utils.py: Contains generic utility functions, including a decorator for memoization.

client.py: The main GitHub client class that uses the utility functions.

fixtures.py: Provides sample data for unit testing.

test_utils.py: Unit tests for the utility functions.

How to Run Tests
To run the unit tests, you will need to install the required libraries:

pip install parameterized

Then, you can run the test file using the python3 -m unittest command:

python3 -m unittest test_utils.py

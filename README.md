# light_detection

Command line tool and API that allows detection of lights in an image.

# Purpose

The purpose of this project is to showcase the way I write and structure python projects to follow PEP8 guidelines, and create reusable, readable, APIs.

# Setup

This project's dependencies are managed by pipenv.
To enter the virtual environment run:

    pipenv shell
    pipenv install

# Run

The command line executable is at ./src/run.py, use the -h switch to view the available options.

# Documentation

The documentation is built using sphinx. To build the documentation run:

    pipenv install --dev
    cd docs
    make html
    cd build/html
    python -m http.server 8000

To view the documentation go to localhost:8000 in a browser.

To build the pdf version of the documentation, traverse to the docs directory and run:

    sphinx-build -b rinoh source build/rinoh

The pdf will be located at docs/build/rinoh/light_detect.pdf

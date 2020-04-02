[![Build Status](https://travis-ci.org/kerenso/brainz.svg?branch=master)](https://travis-ci.org/kerenso/brainz)
[![Documentation Status](https://readthedocs.org/projects/brainz/badge/?version=latest)](https://brainz.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/kerenso/brainz/branch/master/graph/badge.svg)](https://codecov.io/gh/kerenso/brainz)

# Brainz
Project for Advanced System Design Course at Tel Aviv University.
See [full documentation](https://brainz.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:kerenso/brainz.git
    ...
    $ cd brainz/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brainz] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```

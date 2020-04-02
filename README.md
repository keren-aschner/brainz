![Build Status](https://travis-ci.org/kerenso/brainz.svg?branch=master)
![coverage](https://codecov.io/github/kerenso/brainz/branch/master/graph/badge.svg)

# brainz
Project for Advanced System Design Course at Tel Aviv University.
See [full documentation](https://brain-computer-interface.readthedocs.io/en/latest/).

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

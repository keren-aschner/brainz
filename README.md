![Build Status](https://travis-ci.com/kerenso/brain-computer-interface.svg?branch=master)
![coverage](https://codecov.io/github/kerenso/brain-computer-interface/branch/master/graph/badge.svg)

# brain-computer-interface
Project for Advanced System Design Course at Tel Aviv University.
See [full documentation](https://brain-computer-interface.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:kerenso/brain-computer-interface.git
    ...
    $ cd brain-computer-interface/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brain-computer-interface] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```

Brain Computer Interface CLI Reference
======================================

The ``brain_computer_interface`` package provides a command-line interface:


Usage: brain_computer_interface [OPTIONS] COMMAND [ARGS]...

Options:
  --version        Show the version and exit.
  -q, --quiet
  -t, --traceback
  --help           Show this message and exit.

Commands:
  run-server
  run-webserver
  upload-thought



.. code:: bash

    $ python -m brain_computer_interface [OPTIONS] COMMAND [ARGS]...
    ...

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

To see its version, run:

.. code:: bash

    $ python -m brain_computer_interface --version
    brain_computer_interface, version 0.1.0

The ``run-server`` Command
--------------------------

To run the ``run-server`` command:

.. code:: bash

    $ python -m brain_computer_interface run-server [OPTIONS]

Options:
  --address TEXT  The address to run the server on.
  --data TEXT     The data directory
  --help          Show this message and exit.

The ``upload-thought`` Command
------------------------------

To run the ``upload-thought`` command:

.. code:: bash

    $ python -m brain_computer_interface upload-thought [OPTIONS]

Options:
  --address TEXT  The address to upload the thought to.
  --user TEXT     The use id.
  --thought TEXT  The thought to upload.
  --help          Show this message and exit.

The ``run-webserver`` Command
-----------------------------

To run the ``run-webserver`` command:

.. code:: bash

    $ python -m brain_computer_interface run-webserver [OPTIONS]

Options:
  --address TEXT   The address of the webserver.
  --data-dir TEXT  The data dir to expose on the website.
  --help           Show this message and exit.

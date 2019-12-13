Brain Computer Interface API Reference
====================

This is Brain Computer Interface's API reference.

Thought
---

.. class:: brain_computer_interface.utils.Thought

    Encapsulates ``Thought`` objects.

    .. method:: serialize()

        Returns serialized thought object.

    .. method:: deserialize(data)

        Returns a thought object deserialized from ``data``.

upload_thought
---

.. method::  upload_thought(address, user, thought)

    Sends the given thought of the user to the server on the given address.

run_server
---

.. method::  run_server(address, data)

    Run the server on the given address, save the thoughts to the given data dir.

run_webserver
---

.. method::  run_webserver(address, data_dir)

    Run the web server on the given address, expose the thoughts from the given data dir.

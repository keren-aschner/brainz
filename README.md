[![Build Status](https://travis-ci.org/kerenso/brainz.svg?branch=master)](https://travis-ci.org/kerenso/brainz)
[![Documentation Status](https://readthedocs.org/projects/brainz/badge/?version=latest)](https://brainz.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/kerenso/brainz/branch/master/graph/badge.svg)](https://codecov.io/gh/kerenso/brainz)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Brainz
Project for [Advanced System Design](https://advanced-system-design.com/) Course at Tel Aviv University.
See [full documentation](https://brainz.readthedocs.io/en/latest/).

## Installation
1. Clone the repository and enter it:
    ```shell script
    $ git clone git@github.com:kerenso/brainz.git
    ...
    $ cd brainz/
    ```
2. Run the installation script and activate the virtual environment:
    ```shell script
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brainz] $ # you're good to go!
    ```
3. To check that everything is working as expected, run the tests:
    ```shell script
    $ pytest tests/
    ...
    ```

## Running the system 
Make sure you have `docker` and `docker-compose` installed, then run the `scripts/run-pipeline.sh` script.
It uses docker-compose to build and run all the system containers. Once all the containers are up, you can use the
`brainz.client` and `brainz.cli` CLIs as described below. You can also browse the brainz gui at http://localhost:8080/.

## Usage
### The Client
The client reads the sample and uploads it to the server. It is available as `brainz.client` and exposes the following API:
```python
from brainz.client import upload_sample
upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz', protobuf=True)
# upload path to host:port
```
And the following CLI:
```shell script
python -m brainz.client upload-sample \
      -h/--host '127.0.0.1'           \
      -p/--port 8000                  \
      'snapshot.mind.gz'
```

### The Server
The server accepts a connection, receives the uploaded samples and publishes them to its message queue.
It is available as `brainz.server` and exposes the following API:
```python
from brainz.server import run_server
def print_message(message):
    print(message)
run_server(host='127.0.0.1', port=8000, publish=print_message)
# listen on host:port and pass received messages to publish
```
And the following CLI:
```shell script
python -m brainz.server run-server \
      -h/--host '127.0.0.1'        \
      -p/--port 8000               \
      'rabbitmq://127.0.0.1:5672/'
```
The URL is of the form `mq-scheme://host:port`.

### The Parsers
The parsers are simple functions or classes, that are easily deployable as microservices consuming raw data from the 
queue, and producing parsed results to it. They are located in `brainz.parsers`, and expose the following API:
```python
from brainz.parsers import parse
data = '...' 
result = parse('pose', data)
```
Which accepts a parser name and some raw data, as consumed from the message queue, and returns the result, as published 
to the message queue. They also provide the following CLI:
```shell script
python -m brainz.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
```
Which accepts a parser name and a path to some raw data, as consumed from the message queue, and prints the result, as
published to the message queue (optionally redirecting it to a file). This way of invocation runs the parser exactly
once. The CLI also supports running the parser as a service, which works with a message queue indefinitely.
```shell script
python -m brainz.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
```
The implemented parsers are:
 - `Pose` - Collects the translation and the rotation of the user's head at a given timestamp, and publishes the result
 to a dedicated topic.
 - `Color Image` - Collects the color image of what the user was seeing at a given timestamp, and publishes the result
 to a dedicated topic. Note: the data itself is stored to disk, and only the metadata published.
 - `Depth Image` - Collects the depth image of what the user was seeing at a given timestamp, and publishes the result
 to a dedicated topic. Note: the data itself is stored to disk, and only the metadata published.
 - `Feelings` - Collects the feelings the user was experiencing at any timestamp, and publishes the result to a
 dedicated topic.

#### How To Add A New Parser
To add a new parser, use the `add_parser.py` script from the `scripts` directory.
```
Usage: python scripts/add_parser.py [OPTIONS] PARSER_NAME

  Add a parser named PARSER_NAME. Add class if class-parser flag is on,
  otherwise add method.

Options:
  -c, --class-parser  Add class parser.
  --help              Show this message and exit.
```
### The Saver
The saver is available as `brainz.saver` and exposes the following API:
```python
from brainz.saver import Saver
saver = Saver('mongodb://127.0.0.1:27017')
data = '...'
saver.save('pose', data)
```
Which connects to a database, accepts a topic name and some data, as consumed from the message queue, and saves it to
the database. It also provides the following CLI:
```shell script
python -m brainz.saver save                     \
      -d/--database 'mongodb://127.0.0.1:27017' \
     'pose'                                     \
     'pose.result' 
```
Which accepts a topic name and a path to some raw data, as consumed from the message queue, and saves it to a database.
This way of invocation runs the saver exactly once.The CLI also supports running the saver as a service, which works
with a message queue indefinitely.
```shell script
python -m brainz.saver run-saver  \
      'mongodb://127.0.0.1:27017' \
      'rabbitmq://127.0.0.1:5672'
```
The URL is of the form `db-scheme://host:port`.

### The API
The API is available as `brainz.api` and exposes the following API:
```python
from brainz.api import run_api_server
run_api_server(host='127.0.0.1', port=5000,database_url='mongodb://127.0.0.1:27017')
# listen on host:port and serve data from database_url
```
And the following CLI:
```shell script
python -m brainz.api run-server \
      -h/--host '127.0.0.1'     \
      -p/--port 5000            \
      -d/--database 'mongodb://127.0.0.1:27017'
```
The API server supports the following RESTful API endpoints:
- `GET /users` returns the list of all the supported users, including their IDs and names only.
- `GET /users/user-id` returns the specified user's details: ID, name, birthday and gender.
- `GET /users/user-id/snapshots` returns the list of the specified user's snapshot IDs and datetimes only.
- `GET /users/user-id/snapshots/snapshot-id` returns the specified snapshot's details: ID, datetime, and the available
results' names only (e.g. pose).
- `GET /users/user-id/snapshots/snapshot-id/result-name` returns the specified snapshot's result (supports pose,
color-image, depth-image and feelings). 
- `GET /users/user-id/snapshots/snapshot-id/result-name/data` returns the data of results with large binary data
(color-image, depth-image). 

### The CLI
The CLI consumes the API, and reflects it. It is available as `brainz.cli`.

```shell script
python -m brainz.cli get-users
python -m brainz.cli get-user 1
python -m brainz.cli get-snapshots 1
python -m brainz.cli get-snapshot 1 2
python -m brainz.cli get-result 1 2 'pose'
```
All commands accept the -h/--host and -p/--port flags to configure the host and port of the api.
The get-result command also accepts the -s/--save flag that, if specified, receives a path, and saves the result's data
to that path.

### The GUI
The GUI consumes the API and reflects it (using React), it provides the following API/CLI:
```python
from brainz.gui import run_server
run_server(host='127.0.0.1', port=8080, api_host='127.0.0.1', api_port=5000)
```
```shell script
python -m brainz.gui run-server \
      -h/--host '127.0.0.1'     \
      -p/--port 8080            \
      -H/--api-host '127.0.0.1' \
      -P/--api-port 5000
```

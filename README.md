# deepstream.io-client-python

[![Build Status](https://travis-ci.org/VojtechBartos/deepstream.io-client-python.svg?branch=master)](https://travis-ci.org/VojtechBartos/deepstream.io-client-python)

Python client using the dsh HTTP API

## Installation

```sh
pip install git+https://github.com/VojtechBartos/deepstream.io-client-python.git#egg=deepstreamio_client

# this won't work, haven't submitted package to pypi yet
# pip install deepstreamio_client
```

## Examples

```py
from deepstreamio_client import Client

client = Client("https://api.deepstreamhub.com/api/v1", {
    "token": "xxxx-xxxx-xxxx-xxxx"
})
```

### Non batched request

Each separate statement sending new API call

```py
response = client.set_record('user/johndoe', {"name": "John Doe"})

response = client.emit_event("refresh_users")

response = client.make_rpc("remove_user")
```

### Batched request

Set of batch operations that will be executed as a single request

```py
response = client \
    .start_batch()
    .set_record('user/johndoe', {"name": "John Doe"}) \
    .emit_event("refresh_users") \
    .make_rpc("remove_user") \
    .execute_batch() \
    .reset_batch()
```

## Todo's

- documentation
- coverage

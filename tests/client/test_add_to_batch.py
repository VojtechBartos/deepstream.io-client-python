import pytest

from deepstreamio_client import Client

request = {
    'topic': 'record',
    'action': 'read',
    'recordName': 'some-record',
}


def test_adding_to_not_created_batch():
    client = Client("http://url.com")

    with pytest.raises(AssertionError):
        client.add_to_batch(request)


def test_adding_to_created_batch():
    additional_request = {
        'topic': 'record',
        'action': 'delete',
        'recordName': 'some-record',
    }

    client = Client("http://url.com")
    client.start_batch()

    assert client.is_batched
    assert client._batch == []
    assert client.add_to_batch(request)._batch == [request]
    assert client.add_to_batch(additional_request)._batch == [
        request,
        additional_request
    ]

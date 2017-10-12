from deepstreamio_client import Client


def test_starting_batch():
    client = Client("http://url.com")
    assert client._batch is None
    assert client.start_batch()._batch == []

from deepstreamio_client import Client


def test_is_not_batched():
    client = Client("http://url.com")

    assert client.is_batched is False


def test_is_batched():
    client = Client("http://url.com")

    assert client.start_batch().is_batched is True

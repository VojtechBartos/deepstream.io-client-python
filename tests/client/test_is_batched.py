from optx.lib.deepstream import DeepstreamClient


def test_is_not_batched():
    client = DeepstreamClient("http://url.com")

    assert client.is_batched is False


def test_is_batched():
    client = DeepstreamClient("http://url.com")

    assert client.start_batch().is_batched is True

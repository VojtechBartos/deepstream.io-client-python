from optx.lib.deepstream import DeepstreamClient


def test_starting_batch():
    client = DeepstreamClient("http://url.com")
    assert client._batch is None
    assert client.start_batch()._batch == []

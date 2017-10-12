from optx.lib.deepstream import DeepstreamClient


def test_resetting_batch():
    request = {
        'topic': 'record',
        'action': 'read',
        'recordName': 'some-record',
    }

    client = DeepstreamClient("http://url.com")
    client.start_batch().add_to_batch(request)

    assert client.start_batch().add_to_batch(request)._batch == [request]
    assert client.reset_batch()._batch is None

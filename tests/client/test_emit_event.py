from deepstream_client import DeepstreamClient

URL = "http://url.com/"
REQUEST = {
    'topic': 'event',
    'action': 'emit',
    'eventName': 'event-name',
    'data': None
}
REQUEST_WITH_DATA = {
    'topic': 'event',
    'action': 'emit',
    'eventName': 'event-name',
    'data': {"1": 1}
}


def test_not_batched(mocker):
    client = DeepstreamClient(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # success without data
    client._execute.return_value = (True, [{
        "success": True,
        "data": 7
    }])
    assert client.emit_event(REQUEST['eventName'])
    client._execute.assert_called_with([REQUEST])

    # success with data
    client._execute.return_value = (True, [{
        "success": True,
    }])
    assert client.emit_event(REQUEST['eventName'], REQUEST_WITH_DATA['data'])
    client._execute.assert_called_with([REQUEST_WITH_DATA])

    # false response with data
    client._execute.return_value = (False, [{"success": False}])
    assert not client.emit_event(
        REQUEST['eventName'], REQUEST_WITH_DATA['data']
    )
    client._execute.assert_called_with([REQUEST_WITH_DATA])


def test_batched(mocker):
    client = DeepstreamClient(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # with data
    assert isinstance(
        client.start_batch().emit_event(
            REQUEST['eventName'], REQUEST_WITH_DATA['data']
        ),
        DeepstreamClient
    )
    assert client._batch == [REQUEST_WITH_DATA]
    client._execute.assert_not_called()

    # without data
    assert isinstance(
        client.start_batch().emit_event(REQUEST['eventName']),
        DeepstreamClient
    )
    assert client._batch == [REQUEST]
    client._execute.assert_not_called()

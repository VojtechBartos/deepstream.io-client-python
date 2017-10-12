from deepstream_client import DeepstreamClient

URL = "http://url.com/"
REQUEST = {
    'topic': 'record',
    'action': 'head',
    'recordName': 'record-name',
}


def test_not_batched(mocker):
    client = DeepstreamClient(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # success without data
    client._execute.return_value = (True, [{
        "success": True,
        "version": 6
    }])
    assert client.get_record_version(REQUEST['recordName']) == 6
    client._execute.assert_called_with([REQUEST])

    # false response with data
    client._execute.return_value = (False, [{
        "sucess": False
    }])
    assert client.get_record_version(REQUEST['recordName']) is None
    client._execute.assert_called_with([REQUEST])


def test_batched(mocker):
    client = DeepstreamClient(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # without data
    assert isinstance(
        client.start_batch().get_record_version(REQUEST['recordName']),
        DeepstreamClient
    )
    assert client._batch == [REQUEST]
    client._execute.assert_not_called()

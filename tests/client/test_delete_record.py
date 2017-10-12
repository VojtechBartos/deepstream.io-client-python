from deepstreamio_client import Client

URL = "http://url.com/"
REQUEST = {
    'topic': 'record',
    'action': 'delete',
    'recordName': 'record-name',
}


def test_not_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # success without data
    client._execute.return_value = (True, [])
    assert client.delete_record(REQUEST['recordName'])
    client._execute.assert_called_with([REQUEST])

    # false response with data
    client._execute.return_value = (False, [])
    assert client.delete_record(REQUEST['recordName']) is False
    client._execute.assert_called_with([REQUEST])


def test_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # without data
    assert isinstance(
        client.start_batch().delete_record(REQUEST['recordName']),
        Client
    )
    assert client._batch == [REQUEST]
    client._execute.assert_not_called()

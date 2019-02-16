from deepstreamio_client import Client

URL = "http://url.com/"
REQUEST = {
    'topic': 'list',
    'action': 'read',
    'listName': 'list-name',
}


def test_not_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # success
    client._execute.return_value = (True, [{
        "success": True,
        "data": ["a", "b"]
    }])
    assert client.get_list(REQUEST['listName']) == {
        "success": True,
        "data": ["a", "b"]
    }
    client._execute.assert_called_with([REQUEST])

    # false response
    client._execute.return_value = (True, [{
        "success": False,
        "error": "Some"
    }])
    assert client.get_list(REQUEST['listName']) == {
        "success": False,
        "error": "Some"
    }
    client._execute.assert_called_with([REQUEST])


def test_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    assert isinstance(
        client.start_batch().get_list(REQUEST['listName']),
        Client
    )
    assert client._batch == [REQUEST]
    client._execute.assert_not_called()

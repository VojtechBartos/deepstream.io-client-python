from deepstreamio_client import Client

URL = "http://url.com/"
REQUEST = {
    'topic': 'rpc',
    'action': 'make',
    'rpcName': 'rpc-name',
    'data': None
}
REQUEST_WITH_DATA = {
    'topic': 'rpc',
    'action': 'make',
    'rpcName': 'rpc-name',
    'data': {"1": 1}
}


def test_not_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # success without data
    client._execute.return_value = (True, [{
        "success": True,
        "data": 7
    }])
    assert client.make_rpc(REQUEST['rpcName']) == {
        "success": True,
        "data": 7
    }
    client._execute.assert_called_with([REQUEST])

    # success with data
    client._execute.return_value = (True, [{
        "success": True,
        "data": 7
    }])
    assert client.make_rpc(REQUEST['rpcName'], REQUEST_WITH_DATA['data']) == {
        "success": True,
        "data": 7
    }
    client._execute.assert_called_with([REQUEST_WITH_DATA])

    # false response with data
    client._execute.return_value = (True, [{
        "success": False,
        "error": "Some"
    }])
    assert client.make_rpc(REQUEST['rpcName'], REQUEST_WITH_DATA['data']) == {
        "success": False,
        "error": "Some"
    }
    client._execute.assert_called_with([REQUEST_WITH_DATA])


def test_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # with data
    assert isinstance(
        client.start_batch().make_rpc(
            REQUEST['rpcName'], REQUEST_WITH_DATA['data']
        ),
        Client
    )
    assert client._batch == [REQUEST_WITH_DATA]
    client._execute.assert_not_called()

    # without data
    assert isinstance(
        client.start_batch().make_rpc(REQUEST['rpcName']),
        Client
    )
    assert client._batch == [REQUEST]
    client._execute.assert_not_called()

from datetime import datetime

import pytest

from deepstreamio_client import Client

URL = "http://url.com/"
REQUEST = {
    'topic': 'record',
    'action': 'write',
    'recordName': 'record-name',
    'data': {'1': 1}
}


def test_not_json_serializable_record_data():
    client = Client(URL)
    with pytest.raises(TypeError):
        client.set_record('record', datetime.utcnow())


def test_not_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # success with data
    client._execute.return_value = (True, [{
        "success": True,
    }])
    assert client.set_record(REQUEST['recordName'], REQUEST['data']) == {
        "success": True,
    }
    client._execute.assert_called_with([REQUEST])

    # false response with data
    client._execute.return_value = (True, [{
        "success": False,
        "error": "Some"
    }])
    assert client.set_record(REQUEST['recordName'], REQUEST['data']) == {
        "success": False,
        "error": "Some"
    }
    client._execute.assert_called_with([REQUEST])


def test_batched(mocker):
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # with data
    assert isinstance(
        client.start_batch().set_record(
            REQUEST['recordName'], REQUEST['data']
        ),
        Client
    )
    assert client._batch == [REQUEST]
    client._execute.assert_not_called()

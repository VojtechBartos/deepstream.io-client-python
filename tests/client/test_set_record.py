import pytest

from deepstream_client import DeepstreamClient

URL = "http://url.com/"
REQUEST = {
    'topic': 'record',
    'action': 'write',
    'recordName': 'record-name',
    'data': {'1': 1}
}


def test_data_correct_type():
    client = DeepstreamClient(URL)
    invalid = [
        [],
        True,
        None,
        1,
        "hoj"
    ]
    for item in invalid:
        with pytest.raises(AssertionError):
            client.set_record('record', item)


def test_not_batched(mocker):
    client = DeepstreamClient(URL)
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
    client = DeepstreamClient(URL)
    client.auth_data = {"token": "some-token"}

    mocker.patch.object(client, '_execute')

    # with data
    assert isinstance(
        client.start_batch().set_record(
            REQUEST['recordName'], REQUEST['data']
        ),
        DeepstreamClient
    )
    assert client._batch == [REQUEST]
    client._execute.assert_not_called()

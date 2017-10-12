import pytest
import requests_mock

from deepstreamio_client import Client, DeepstreamioHTTPError

URL = "http://url.com/"


def test_not_batched():
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    # success
    with requests_mock.mock() as m:
        m.post(URL, status_code=200, json={
            'result': 'SUCCESS',
            'body': [{
                "success": True,
                "data": "hoj"
            }]
        })
        body = [{
            'topic': 'record',
            'action': 'head',
            'recordName': 'record-name',
        }]
        assert client._execute(body) == (
            True,
            [{
                "success": True,
                "data": "hoj"
            }]
        )

    # success
    with requests_mock.mock() as m:
        m.post(URL, status_code=200, json={
            'result': 'FAILURE',
            'body': [{
                "success": False,
                "error": "Some"
            }]
        })
        body = [{
            'topic': 'record',
            'action': 'head',
            'recordName': 'record-name',
        }]
        assert client._execute(body) == (
            False,
            [{
                "success": False,
                "error": "Some"
            }]
        )


def test_batched():
    client = Client(URL)
    client.auth_data = {"token": "some-token"}
    client.start_batch()
    client.get_record("recordName")
    client.make_rpc("rpcName")
    client.emit_event("eventName")

    assert client._batch == [
        {
            'action': 'read',
            'recordName': 'recordName',
            'topic': 'record'},
        {
            'action': 'make',
            'data': None,
            'rpcName': 'rpcName',
            'topic': 'rpc'
        },
        {
            'action': 'emit',
            'data': None,
            'eventName': 'eventName',
            'topic': 'event'
        }
    ]

    with requests_mock.mock() as m:
        res = {
            'result': "SUCCESS",
            'body': [
                {"success": True, "data": "data"},
                {"success": True},
                {"success": True}
            ]
        }
        m.post(URL, status_code=200, json=res)

        assert client.execute_batch() == res['body']


def test_invalid_request():
    client = Client(URL)
    client.auth_data = {"token": "some-token"}

    with requests_mock.mock() as m:
        m.post(URL, status_code=400, text="Some error")

        with pytest.raises(DeepstreamioHTTPError):
            client._execute([{"something": "something"}])

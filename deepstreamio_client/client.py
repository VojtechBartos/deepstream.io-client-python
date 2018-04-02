import requests

from .exceptions import DeepstreamioHTTPError


class Client:
    """The deepstream Python client running against the dsh/dsx HTTP API"""

    def __init__(self, url, auth_data=None):
        """Constructs the client
        :param url: {str} HTTP(S) URL for a deepstream endpoint
        :param auth_data: {dict} any authentication information
        """
        self.url = url
        self.auth_data = auth_data or {}
        self._batch = None

    def start_batch(self):
        """Initiates a set of batch operations. No actual request will be sent
        until executeBatch is called
        :return: {Client}
        """
        self._batch = []
        return self

    def execute_batch(self):
        """Executes a set of batch operations
        :return: {list} with body items from a response
        """
        assert isinstance(self._batch, list)

        success, body = self._execute(self._batch)
        if success:
            self.reset_batch()

        return body

    def clear_batch(self):
        """Clear batch, empty items in the batch
        :return: {Client}
        """
        self._batch = []
        return self

    def reset_batch(self):
        """Reset batch, stopping doing batch request(s)
        :return: {Client}
        """
        self._batch = None
        return self

    @property
    def is_batched(self):
        """Detecting if the batch has been started or is in progress
        :return: {bool}
        """
        return isinstance(self._batch, list)

    def add_to_batch(self, request):
        """Adding a request body to batch
        :return: {Client}
        """
        assert isinstance(self._batch, list)

        self._batch.append(request)
        return self

    def get_record(self, name):
        """Retrieves data for a single record
        :param name: {str} record name
        :return: {Client} for a batch and JSON serializable object for
                          non-batch
        """
        request = {
            'topic': 'record',
            'action': 'read',
            'recordName': name,
        }
        if self.is_batched:
            return self.add_to_batch(request)

        _, body = self._execute([request])
        return body[0]

    def set_record(self, name, data, path=None):
        """Updates a records data. Can be called with a path for partial updates
        :param name: {str} record name
        :param data: JSON serializable object
        :param path: {str} optional path
        :return: {Client} for a batch and {bool} for non-batch
        """
        request = {
            'topic': 'record',
            'action': 'write',
            'recordName': name,
            'data': data
        }
        if path:
            request['path'] = path

        if self.is_batched:
            return self.add_to_batch(request)

        _, body = self._execute([request])
        return body[0]

    def delete_record(self, name):
        """Deletes a record
        :param name: {str} record name
        :return: {Client} for a batch and {bool} for non-batch
        """
        request = {
            'topic': 'record',
            'action': 'delete',
            'recordName': name
        }
        if self.is_batched:
            return self.add_to_batch(request)

        success, _ = self._execute([request])
        return success

    def get_record_version(self, name):
        """Returns the current version for a record
        :param name: {str} record name
        :return: {Client} for a batch and {int} for non-batch
        """
        request = {
            'topic': 'record',
            'action': 'head',
            'recordName': name,
        }
        if self.is_batched:
            return self.add_to_batch(request)

        success, body = self._execute([request])
        if not success:
            return

        return body[0]['version']

    def make_rpc(self, name, data=None):
        """Executes a Remote Procedure Call
        :param name: {str} record name
        :param data: JSON serializable object
        :return: {Client} for a batch and JSON serializable object for
                          non-batch
        """
        request = {
            'topic': 'rpc',
            'action': 'make',
            'rpcName': name,
            'data': data
        }
        if self.is_batched:
            return self.add_to_batch(request)

        success, body = self._execute([request])

        return body[0]

    def emit_event(self, name, data=None):
        """Emits a deepstream event
        :param name: {str} record name
        :param data: JSON serializable object
        :return: {Client} for a batch and {bool} for non-batch
        """
        request = {
            'topic': 'event',
            'action': 'emit',
            'eventName': name,
            'data': data
        }
        if self.is_batched:
            return self.add_to_batch(request)

        success, _ = self._execute([request])
        return success

    def _execute(self, body):
        payload = {"body": body}
        payload.update(self.auth_data)

        try:
            res = requests.post(self.url, json=payload)
            res.raise_for_status()
            data = res.json()
            status = all([
                res.status_code == requests.codes.ok,
                data.get('result') == 'SUCCESS'
            ])
        except requests.exceptions.HTTPError as e:
            raise DeepstreamioHTTPError("%s: %s" % (
                e.response.status_code, e.response.text
            ))

        return status, data.get('body', [])

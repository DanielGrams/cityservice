import pathlib
from datetime import datetime

from flask import url_for


class UtilActions(object):
    def __init__(self, client, app, mocker, requests_mock):
        self._client = client
        self._app = app
        self._mocker = mocker
        self._requests_mock = requests_mock
        self._feedparser_mapping = dict()

    def get_url(self, endpoint, **values):
        with self._app.test_request_context():
            url = url_for(endpoint, **values, _external=False)
        return url

    def get(self, url):
        response = self._client.get(url)
        return response

    def get_ok(self, url):
        response = self.get(url)
        self.assert_response_ok(response)
        return response

    def get_endpoint(self, endpoint, **values):
        return self._client.get(self.get_url(endpoint, **values))

    def get_endpoint_ok(self, endpoint, **values):
        return self.get_ok(self.get_url(endpoint, **values))

    def assert_response_ok(self, response):
        assert response.status_code == 200

    def mock_get_request_with_text(self, url: str, text: str):
        self._requests_mock.get(url, text=text)

    def mock_get_request_with_content(self, url: str, content):
        self._requests_mock.get(url, content=content)

    def mock_get_request_with_file(self, url: str, path: pathlib.Path, filename: str):
        text = (path / filename).read_text()
        self.mock_get_request_with_text(url, text)

    def mock_feedparser_http_get(
        self, url: str = None, path: pathlib.Path = None, filename: str = None
    ):
        if url:
            byte_text = (path / filename).read_bytes()
            self._feedparser_mapping[url] = byte_text

        def get_patch(
            url,
            etag=None,
            modified=None,
            agent=None,
            referrer=None,
            handlers=None,
            request_headers=None,
            result=None,
        ):
            if url in self._feedparser_mapping:
                return self._feedparser_mapping[url]

            raise ValueError("404 Not patched")

        self._mocker.patch("feedparser.http.get", side_effect=get_patch)

    def mock_now(self, year: int, month: int, day: int) -> datetime:
        from project.dateutils import create_berlin_date

        now = create_berlin_date(year, month, day)
        self._mocker.patch("project.dateutils.get_now", return_value=now)
        return now

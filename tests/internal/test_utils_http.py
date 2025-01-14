import httpretty
import pytest

from ddtrace.internal.utils.http import connector
from tests.utils import flaky


@flaky(until=1704067201)
@pytest.mark.parametrize("scheme", ["http", "https"])
def test_connector(scheme):
    with httpretty.enabled():
        httpretty.register_uri(httpretty.GET, "%s://localhost:8181/api/test" % scheme, body='{"hello": "world"}')

        connect = connector("%s://localhost:8181" % scheme)
        with connect() as conn:
            conn.request("GET", "/api/test")
            response = conn.getresponse()
            assert response.status == 200
            assert response.read() == b'{"hello": "world"}'

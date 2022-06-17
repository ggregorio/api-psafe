"""
All application tests will be contained in this file.
"""

import pytest
from app import app

@pytest.fixture
def client():
    """
    Client will set up the DB to a Temp file,
    and leave everything ready to run
    """
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(params=['/healthcheck'])
def health_endpoint(request):
    """
    Will return each endpoint in time, for both
    of them to be tested correctly below
    :param request:
    :return:
    """
    return request.param


def test_health_checks(client, health_endpoint):
    """ Ensure the healthcheck endpoints are working correctly """
    resp = client.get(health_endpoint)
    assert resp.status_code == 200

from starlette import status
from src.core.routes import Routes
from tests.test_database import clint
from tests.testing_json import root_route_expected_response


def test_read_users():
    response = clint.get(Routes.ROOT_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == root_route_expected_response

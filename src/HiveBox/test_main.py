from fastapi.testclient import TestClient
from .main import app
import re
import pytest

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    regex_pattern = "^(?P<major>0|[1-9]\\d*)\\.(?P<minor>0|[1-9]\\d*)\\.(?P<patch>0|[1-9]\\d*)(?:-(?P<prerelease>(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    assert re.match(regex_pattern, response.json()["message"]) is not None


def test_get_temperature():
    response = client.get("/temperature")
    assert response.status_code == 200
    assert can_be_float(response.json()["message"])


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("123", True),
        ("3.14", True),
        ("-7.5", True),
        ("1e5", True),  # scientific notation
        ("abc", False),
        ("", False),
        ("   ", False),
        ("NaN", True),
        ("inf", True),
        ("-inf", True),
    ],
)
def test_can_be_float(input_str, expected):
    assert can_be_float(input_str) == expected


def can_be_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

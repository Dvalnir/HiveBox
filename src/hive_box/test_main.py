"""
Test module for the hive_box application.
"""

import re
from fastapi.testclient import TestClient
import pytest
from .main import app

client = TestClient(app)


def test_get_root():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_version():
    """
    Test the version endpoint.
    """
    response = client.get("/version")
    assert response.status_code == 200
    # pylint: disable=line-too-long
    regex_pattern = "^(?P<major>0|[1-9]\\d*)\\.(?P<minor>0|[1-9]\\d*)\\.(?P<patch>0|[1-9]\\d*)(?:-(?P<prerelease>(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    assert re.match(regex_pattern, response.json()["message"]) is not None


def test_get_temperature():
    """
    Test the temperature endpoint.
    """
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
    """
    Test the can_be_float function.
    """
    assert can_be_float(input_str) == expected


def can_be_float(input_string):
    """
    Determines if a given string can be converted to a float.

    Args:
        input_string (str): The string to be evaluated.

    Returns:
        bool: True if the string can be successfully converted to a float,
              False if it raises a ValueError during conversion.
    """
    try:
        float(input_string)
        return True
    except ValueError:
        return False

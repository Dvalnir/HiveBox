"""
Temperature endpoint module.
"""

from datetime import datetime, timedelta, timezone
from statistics import fmean
import asyncio
import aiohttp
from fastapi import APIRouter

router = APIRouter()


@router.get("/temperature")
async def temperature():
    """Return current average temperature based on all senseBox data."""
    return {"message": f"{await get_average_temp()}"}


async def get_average_temp() -> float:
    """
    Retrieve current senseBox temperatures and calculate average temperature.
    """
    sensebox_id_list = [
        "5eba5fbad46fb8001b799786",
        "5c21ff8f919bf8001adf2488",
        "5ade1acf223bd80019a1011c",
    ]

    sensebox_list_data = await retrieve_sensebox_list_data(sensebox_id_list)

    # Create a temperature_list
    temperature_list = []
    measurement_last_acceptable_time = datetime.now(timezone.utc) - timedelta(hours=1)
    for response in sensebox_list_data:
        temp = extract_box_temp(measurement_last_acceptable_time, response)
        if temp is not None:
            temperature_list.append(temp)

    # Return the average or 0 Kelvin if list is empty
    if len(temperature_list) == 0:
        return -273.15
    return fmean(temperature_list)


async def retrieve_sensebox_list_data(sensebox_id_list: list[str]):
    """
    Asynchronously retrieves data for a list of senseBox IDs from the OpenSenseMap API.

    This function sends concurrent GET requests to the OpenSenseMap API to fetch the data
    for each senseBox ID in the provided list. It collects the results and returns the data
    as a list of JSON responses, one for each valid senseBox.

    Args:
        sensebox_id_list (list[str]): A list of senseBox IDs for which data should be retrieved.

    Returns:
        list[dict]: A list of dictionaries containing the JSON response data for each senseBox,
                    or an empty list if no data could be retrieved.

    Notes:
        - If a request fails (i.e., status code is not 200), an error message is printed,
          and the corresponding data is not included in the response.
        - The request timeout for each API call is set to 10 seconds.
    """
    request_timeout = aiohttp.ClientTimeout(total=10)
    json_list: list[dict] = []
    async with aiohttp.ClientSession(timeout=request_timeout) as session:
        session_list: list[aiohttp.ClientSession] = []
        for sensebox_id in sensebox_id_list:
            api_url = f"https://api.opensensemap.org/boxes/{sensebox_id}"
            session_list.append(session.get(api_url))
        session_list = await asyncio.gather(*session_list)
        for session in session_list:
            if session.status == 200:
                json_list.append(session.json())
            else:
                print(f"{session._base_url} resulted in status code {session.status}")  # pylint: disable=protected-access
        json_list = await asyncio.gather(*json_list)
    return json_list


def extract_box_temp(
    measurement_last_acceptable_time: datetime, extracted_response: dict
):
    """
    Extracts the temperature from the senseBox measurement if it meets the time criteria.

    Args:
        measurement_last_acceptable_time (datetime): The latest acceptable time for the measurement.
        extracted_response (dict): A dictionary containing the extracted sensor data.

    Returns:
        float | None: The temperature value if the measurement is within the acceptable time range,
                      or None if it is outside that range.
    """
    last_measurement = extract_last_measurement(extracted_response)
    return filter_on_time(measurement_last_acceptable_time, last_measurement)


def extract_last_measurement(extracted_response: dict) -> dict | None:
    """
    Extracts the last temperature measurement from the response data.

    Args:
        extracted_response (dict): A dictionary containing the extracted sensor data.

    Returns:
        dict | None: The last temperature measurement from the "Temperatur" sensor or
                     None if nothing was found.
    """
    for sensor in extracted_response["sensors"]:
        if sensor["title"] == "Temperatur":
            return sensor["lastMeasurement"]
    return None


def filter_on_time(
    measurement_last_acceptable_time: datetime, last_measurement: dict
) -> float | None:
    """
    Filters a temperature measurement based on whether its timestamp is within the acceptable
    time range.

    Args:
        measurement_last_acceptable_time (datetime): The latest acceptable time for the measurement.
        last_measurement (dict): A dictionary containing the last measurement data, including a
        timestamp and value.

    Returns:
        float | None: The temperature value if the measurement timestamp is within the
                      acceptable range, or None if it is outside that range.
    """
    # 2025-04-21T12:55:17.511Z where Z is Zulu time => UTC+0
    opensense_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    measurement_time = datetime.strptime(
        last_measurement["createdAt"], opensense_time_format
    )
    if measurement_time >= measurement_last_acceptable_time:
        return float(last_measurement["value"])
    return None

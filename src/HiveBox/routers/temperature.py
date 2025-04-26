import asyncio
from statistics import fmean
import aiohttp
from fastapi import APIRouter
from datetime import datetime, timedelta, timezone

router = APIRouter()


@router.get("/temperature")
async def temperature():
    """Return current average temperature based on all senseBox data."""
    return {"message": f"{await get_average_temp()}"}


async def get_average_temp() -> float:
    """Retrieve current senseBox temperatures and calculate average temperature."""
    sensebox_ID_list = [
        "5eba5fbad46fb8001b799786",
        "5c21ff8f919bf8001adf2488",
        "5ade1acf223bd80019a1011c",
    ]

    sensebox_list_data = await retrieve_sensebox_list_data(sensebox_ID_list)

    # Create a temperature_list
    temperature_list = []
    measurement_last_acceptable_time = datetime.now(timezone.utc) - timedelta(hours=1)
    for response in sensebox_list_data:
        temp = extract_box_temp(measurement_last_acceptable_time, response)
        if temp is not None:
            temperature_list.append(temp)

    # Return the average or 0K if list is empty
    if len(temperature_list) == 0:
        return -273.15
    else:
        return fmean(temperature_list)


async def retrieve_sensebox_list_data(sensebox_ID_list: list[str]):
    request_timeout = aiohttp.ClientTimeout(total=10)
    json_list: list[dict] = []
    async with aiohttp.ClientSession(timeout=request_timeout) as session:
        session_list: list[aiohttp.ClientSession] = []
        for sensebox_ID in sensebox_ID_list:
            api_url = f"https://api.opensensemap.org/boxes/{sensebox_ID}"
            session_list.append(session.get(api_url))
        session_list = await asyncio.gather(*session_list)
        for session in session_list:
            if session.status == 200:
                json_list.append(session.json())
            else:
                print(f"{session._base_url} resulted in status code {session.status}")
        json_list = await asyncio.gather(*json_list)
    return json_list


def extract_box_temp(
    measurement_last_acceptable_time: datetime, extracted_response: dict
):
    """Retrieve a senseBox temperature."""
    last_measurement = extract_last_measurement(extracted_response)
    return filter_on_time(measurement_last_acceptable_time, last_measurement)


def extract_last_measurement(extracted_response: dict) -> dict:
    for sensor in extracted_response["sensors"]:
        if sensor["title"] == "Temperatur":
            return sensor["lastMeasurement"]


def filter_on_time(
    measurement_last_acceptable_time: datetime, last_measurement: dict
) -> float | None:
    # 2025-04-21T12:55:17.511Z where Z is Zulu time => UTC+0
    opensense_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    measurement_time = datetime.strptime(
        last_measurement["createdAt"], opensense_time_format
    )
    if measurement_time >= measurement_last_acceptable_time:
        return float(last_measurement["value"])
    else:
        return None

from statistics import fmean
import requests
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
    measurement_last_acceptable_time = datetime.now(timezone.utc) - timedelta(hours=1)
    temperature_list = []
    for sensebox_ID in sensebox_ID_list:
        api_url = f"https://api.opensensemap.org/boxes/{sensebox_ID}"
        temp = get_box_temp_if_eligible(measurement_last_acceptable_time, api_url)
        if temp is not None:
            temperature_list.append(temp)
    if len(temperature_list) == 0:
        return -273.15
    else:
        return fmean(temperature_list)


def get_box_temp_if_eligible(measurement_last_acceptable_time, api_url) -> float | None:
    """Retrieve a senseBox temperature."""
    box_temperature = None
    # 2025-04-21T12:55:17.511Z where Z is Zulu time => UTC+0
    opensense_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    request_timeout = 0.3
    result = requests.get(url=api_url, timeout=request_timeout)
    if result.status_code == 200:
        for sensor in result.json()["sensors"]:
            if sensor["title"] == "Temperatur":
                last_measurement = sensor["lastMeasurement"]
                measurement_time = datetime.strptime(
                    last_measurement["createdAt"], opensense_time_format
                )
                if measurement_time >= measurement_last_acceptable_time:
                    box_temperature = float(last_measurement["value"])
    else:
        print(f"{api_url} resulted in status code {result.status_code}")
    return box_temperature

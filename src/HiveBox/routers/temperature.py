from statistics import fmean
import requests
from fastapi import APIRouter
from datetime import datetime, timedelta, timezone

router = APIRouter()


@router.get("/temperature")
async def temperature():
    """Return current average temperature based on all senseBox data."""
    return {"message": f"{await get_average_temp()}"}


async def get_average_temp():
    """Retrieve current senseBox temperatures and calculate average temperature."""
    sensebox_ID_list = [
        "5eba5fbad46fb8001b799786",
        "5c21ff8f919bf8001adf2488",
        "5ade1acf223bd80019a1011c",
    ]
    measurement_last_acceptable_time = datetime.now(timezone.utc) - timedelta(hours=1)
    # 2025-04-21T12:55:17.511Z where Z is Zulu time => UTC+0
    opensense_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    temperature_list = []
    for sensebox_ID in sensebox_ID_list:
        api_url = f"https://api.opensensemap.org/boxes/{sensebox_ID}"
        result = requests.get(url=api_url, timeout=0.3)
        if result.status_code == 200:
            for sensor in result.json()["sensors"]:
                if sensor["title"] == "Temperatur":
                    last_measurement = sensor["lastMeasurement"]
                    measurement_time = datetime.strptime(
                        last_measurement["createdAt"], opensense_time_format
                    )
                    if measurement_time >= measurement_last_acceptable_time:
                        temperature_list.append(float(last_measurement["value"]))
        else:
            print(f"{api_url} resulted in status code {result.status_code}")
    if len(temperature_list) == 0:
        return -273.15
    else:
        return fmean(temperature_list)

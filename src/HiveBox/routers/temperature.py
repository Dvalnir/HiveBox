import requests
from fastapi import APIRouter

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
    average_temperature = 0
    for sensebox_ID in sensebox_ID_list:
        api_url = f"https://api.opensensemap.org/boxes/{sensebox_ID}"
        result = requests.get(url=api_url, timeout=0.3)
        if result.status_code == 200:
            for sensor in result.json()["sensors"]:
                if sensor["title"] == "Temperatur":
                    average_temperature += float(sensor["lastMeasurement"]["value"])
        else:
            print(f"{api_url} resulted in status code {result.status_code}")
    average_temperature /= len(sensebox_ID_list)
    return average_temperature

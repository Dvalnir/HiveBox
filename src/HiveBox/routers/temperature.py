from fastapi import APIRouter

router = APIRouter()

@router.get("/temperature")
async def temperature():
    """Return current average temperature based on all senseBox data."""
    return {"message": "Dummy data"}

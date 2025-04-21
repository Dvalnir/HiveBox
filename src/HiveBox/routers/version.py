from HiveBox import __version__

from fastapi import APIRouter

router = APIRouter()


@router.get("/version")
async def version():
    """Returns the version of the HiveBox app."""
    return {"message": f"{__version__}"}

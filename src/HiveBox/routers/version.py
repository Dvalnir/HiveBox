"""
Version endpoint module.
"""

from fastapi import APIRouter
from HiveBox import __version__

router = APIRouter()


@router.get("/version")
async def version():
    """Returns the version of the HiveBox app."""
    return {"message": f"{__version__}"}

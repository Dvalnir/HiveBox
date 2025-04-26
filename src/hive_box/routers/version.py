"""
Version endpoint module.
"""

from fastapi import APIRouter
from hive_box import __version__

router = APIRouter()


@router.get("/version")
async def version():
    """Returns the version of the hive_box app."""
    return {"message": f"{__version__}"}

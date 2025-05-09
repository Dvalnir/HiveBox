"""
Main module which also define the root endpoint.
"""

from fastapi import FastAPI
from .routers import version, temperature

app = FastAPI()

app.include_router(version.router)
app.include_router(temperature.router)


@app.get("/")
async def root():
    """
    Handle GET requests to the root endpoint.
    """
    return {"message": "Hello World"}

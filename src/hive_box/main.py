"""
Main module which also define the root endpoint.
"""

from fastapi import FastAPI
from prometheus_client import make_asgi_app
from .routers import version, temperature

app = FastAPI()

app.include_router(version.router)
app.include_router(temperature.router)

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
async def root():
    """
    Handle GET requests to the root endpoint.
    """
    return {"message": "Hello World"}

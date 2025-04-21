from fastapi import FastAPI
from .routers import version, temperature

app = FastAPI()

app.include_router(version.router)
app.include_router(temperature.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

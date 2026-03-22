from fastapi import FastAPI
from app.api.routes_plan import router as plan_router

app = FastAPI(title="DevProject AI API")

app.include_router(plan_router)


@app.get("/")
def read_root():
    return {"message": "DevProject AI backend is running"}

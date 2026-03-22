from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_plan import router as plan_router

app = FastAPI(title="DevProject AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan_router)


@app.get("/")
def read_root():
    return {"message": "DevProject AI backend is running"}

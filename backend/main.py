from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

try:
    from .recommender import recommend
except ImportError:
    from recommender import recommend

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"

app = FastAPI(title="Cheat Meal Picker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendRequest(BaseModel):
    target_calories: int = 1200
    cuisine: str = "all"
    exclude_tags: List[str] = []
    include_drink: bool = True
    include_dessert: bool = True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/health")
def api_health():
    return {"status": "ok"}


@app.post("/api/recommend")
def get_recommendations(req: RecommendRequest):
    results = recommend(
        target_calories=req.target_calories,
        cuisine=req.cuisine,
        exclude_tags=req.exclude_tags,
        include_drink=req.include_drink,
        include_dessert=req.include_dessert,
    )
    return {"recommendations": results, "target_calories": req.target_calories}


app.add_api_route("/recommend", get_recommendations, methods=["POST"])

if FRONTEND_DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST_DIR, html=True), name="frontend")

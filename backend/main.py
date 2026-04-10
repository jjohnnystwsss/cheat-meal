from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from recommender import recommend

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


@app.post("/recommend")
def get_recommendations(req: RecommendRequest):
    results = recommend(
        target_calories=req.target_calories,
        cuisine=req.cuisine,
        exclude_tags=req.exclude_tags,
        include_drink=req.include_drink,
        include_dessert=req.include_dessert,
    )
    return {"recommendations": results, "target_calories": req.target_calories}

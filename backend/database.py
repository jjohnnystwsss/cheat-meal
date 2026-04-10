import json
import os
from pathlib import Path

from sqlalchemy import (
    Column, Integer, String, Float, ARRAY,
    create_engine, text
)
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL) if DATABASE_URL else None
except Exception as e:
    print(f"[WARNING] Failed to create DB engine: {e}")
    engine = None


class Base(DeclarativeBase):
    pass


class Food(Base):
    __tablename__ = "foods"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    meal_role = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    protein_g = Column(Float, nullable=False)
    price_twd = Column(Integer, nullable=False)
    tags = Column(ARRAY(String), nullable=False, default=list)


def init_db():
    """Create tables and seed foods.json if the table is empty."""
    if engine is None:
        return

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        count = session.execute(text("SELECT COUNT(*) FROM foods")).scalar()
        if count > 0:
            return

        foods_path = Path(__file__).resolve().parent.parent / "foods.json"
        with open(foods_path, encoding="utf-8") as f:
            foods = json.load(f)["foods"]

        for item in foods:
            session.add(Food(
                id=item["id"],
                name=item["name"],
                brand=item["brand"],
                category=item["category"],
                cuisine=item["cuisine"],
                meal_role=item["meal_role"],
                calories=item["calories"],
                protein_g=item["protein_g"],
                price_twd=item["price_twd"],
                tags=item.get("tags", []),
            ))
        session.commit()


def get_all_foods() -> list[dict]:
    """Return all foods from DB as dicts (same shape as foods.json)."""
    if engine is None:
        return []

    with Session(engine) as session:
        rows = session.query(Food).all()
        return [
            {
                "id": r.id,
                "name": r.name,
                "brand": r.brand,
                "category": r.category,
                "cuisine": r.cuisine,
                "meal_role": r.meal_role,
                "calories": r.calories,
                "protein_g": r.protein_g,
                "price_twd": r.price_twd,
                "tags": r.tags or [],
            }
            for r in rows
        ]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.base import Base, engine, SessionLocal
from .services.seed import seed_initial_data
from .services.tour_loader import load_tour_items_separate_tables as load_tour_items
from .services.tour_translation_loader import load_tour_item_translations
from .services.restaurant_loader import load_restaurant_en_items, load_restaurant_items

from .api.routers import places, posts, restaurants, travel_spots, map

app = FastAPI(title="LocalHub API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def read_health():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as conn:
        seed_initial_data(conn)
        load_tour_items(conn)
        load_tour_item_translations(conn)
        load_restaurant_items(conn)
        load_restaurant_en_items(conn)

# app.include_router(health.router)
app.include_router(places.router)
app.include_router(posts.router)
app.include_router(restaurants.router)
app.include_router(travel_spots.router)
app.include_router(map.router)

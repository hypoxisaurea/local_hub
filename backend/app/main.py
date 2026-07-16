from backend.app.api.routers import weather
from backend.AI.app.chatbot.router import router as chatbot_router
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db.base import Base, engine, SessionLocal
from .services.seed import seed_initial_data
from .services.tour_loader import load_tour_items_separate_tables as load_tour_items
from .services.tour_translation_loader import load_tour_item_translations
from .services.restaurant_loader import load_restaurant_en_items, load_restaurant_items

from .api.routers import posts, restaurants, travel_spots, map
from .crud.posts import ensure_missing_post_en

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
        ensure_missing_post_en(conn)

# app.include_router(health.router)
app.include_router(posts.router)
app.include_router(restaurants.router)
app.include_router(travel_spots.router)
app.include_router(map.router)
app.include_router(weather.router)
app.include_router(chatbot_router, prefix="/api")

DIST_DIR = Path(__file__).resolve().parents[2] / "frontend" / "dist"
INDEX_FILE = DIST_DIR / "index.html"
ASSETS_DIR = DIST_DIR / "assets"

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


@app.get("/")
def serve_index():
    if not INDEX_FILE.exists():
        return {"message": "LocalHub API is running", "docs": "/docs", "health": "/api/health"}

    return FileResponse(INDEX_FILE)


@app.get("/{path:path}")
def serve_spa(path: str):
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")

    if not INDEX_FILE.exists():
        raise HTTPException(status_code=404, detail="Not Found")

    requested_file = DIST_DIR / path
    if requested_file.is_file():
        return FileResponse(requested_file)

    return FileResponse(INDEX_FILE)

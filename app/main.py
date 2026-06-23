from pathlib import Path

import pendulum
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import get_category_label, get_cta, load_trip
from app.weather import get_weather_for_days

BASE_DIR = Path(__file__).parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.globals["get_cta"] = get_cta
templates.env.globals["get_category_label"] = get_category_label

trip = load_trip()

CATEGORY_COLORS = {
    "parking": "#e8a44a",
    "attraction": "#5a8a5e",
    "restaurant": "#c25e3a",
    "hotel": "#7b6b8a",
    "cafe": "#8b6f4e",
    "icecream": "#d4849a",
    "market": "#6a8e7f",
    "viewpoint": "#4a7fa5",
    "beach": "#4ab5c4",
    "playground": "#e8a44a",
    "shopping": "#b07aa1",
    "activity": "#6aaa5e",
    "supermarket": "#5a8a5e",
    "note": "#8a8a7a",
}

templates.env.globals["category_colors"] = CATEGORY_COLORS


def _today_day_number() -> int | None:
    """Return 1-based day number if today falls within the trip dates."""
    now = pendulum.now("Europe/Paris")
    start = pendulum.parse(trip.start_date, tz="Europe/Paris")
    end = pendulum.parse(trip.end_date, tz="Europe/Paris")
    if start <= now <= end.end_of("day"):
        return now.diff(start).in_days() + 1
    return None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    weather = await get_weather_for_days(trip)
    return templates.TemplateResponse(request, "index.html", {
        "trip": trip,
        "weather": weather,
    })


@app.get("/overview", response_class=HTMLResponse)
async def overview(request: Request):
    weather = await get_weather_for_days(trip)
    return templates.TemplateResponse(request, "index.html", {
        "trip": trip,
        "weather": weather,
    })


@app.get("/day/{day_number}", response_class=HTMLResponse)
async def day_view(request: Request, day_number: int):
    if day_number < 1 or day_number > len(trip.days):
        return RedirectResponse(url="/overview", status_code=302)
    day = trip.days[day_number - 1]
    weather = await get_weather_for_days(trip)
    return templates.TemplateResponse(request, "day.html", {
        "trip": trip,
        "day": day,
        "day_number": day_number,
        "total_days": len(trip.days),
        "weather": weather,
    })

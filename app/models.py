"""Pydantic data models for trip itinerary.

Usage:
    # Validate trip.json
    uv run python -m app.models
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import BaseModel


class CityCoords(BaseModel):
    name: str
    latitude: float
    longitude: float
    timezone: str


class ItineraryItem(BaseModel):
    category: str
    name_zh: str
    name_en: str | None = None
    description_zh: str | None = None
    time_of_day: str | None = None
    google_maps_url: str | None = None
    is_backup: bool = False
    cta_label: str | None = None


class DayPlan(BaseModel):
    date: str
    title_zh: str
    title_en: str | None = None
    weekday_zh: str
    summary_zh: str | None = None
    notes: list[str] = []
    items: list[ItineraryItem]
    coords: CityCoords | None = None


class Accommodation(BaseModel):
    name_zh: str
    name_en: str | None = None
    google_maps_url: str | None = None


class Trip(BaseModel):
    title_zh: str
    start_date: str
    end_date: str
    accommodation: Accommodation | None = None
    coords: CityCoords | None = None
    days: list[DayPlan]


def coords_for(trip: Trip, day: DayPlan) -> CityCoords | None:
    return day.coords or trip.coords


DATA_DIR = Path(__file__).parent / "data"


def load_trip() -> Trip:
    with open(DATA_DIR / "trip.json", encoding="utf-8") as f:
        return Trip(**json.load(f))


# Default CTA labels by category
DEFAULT_CTA = {
    "parking": "开车前往 · 导航",
    "attraction": "查看景点位置",
    "restaurant": "点击预定/查看位置",
    "hotel": "查看酒店地图",
    "cafe": "查看位置",
    "icecream": "查看位置",
    "market": "查看位置",
    "viewpoint": "查看位置",
    "beach": "查看位置",
    "playground": "查看位置",
    "shopping": "查看位置",
    "activity": "查看位置",
}


def get_cta(item: ItineraryItem) -> str:
    if item.cta_label:
        return item.cta_label
    return DEFAULT_CTA.get(item.category, "查看位置")


# Category display names
CATEGORY_LABELS = {
    "parking": ("PARKING", "停车场"),
    "attraction": ("ATTRACTION", "景点"),
    "restaurant": ("RESTAURANT", "餐厅"),
    "hotel": ("HOTEL", "酒店"),
    "cafe": ("CAFÉ", "咖啡"),
    "icecream": ("ICE CREAM", "冰淇淋"),
    "market": ("MARKET", "市场"),
    "viewpoint": ("VIEWPOINT", "观景台"),
    "beach": ("BEACH", "海滩"),
    "playground": ("PLAYGROUND", "游乐场"),
    "shopping": ("SHOPPING", "购物"),
    "activity": ("ACTIVITY", "活动"),
    "supermarket": ("SUPERMARKET", "超市"),
    "note": ("NOTE", "备注"),
}


def get_category_label(category: str) -> tuple[str, str]:
    return CATEGORY_LABELS.get(category, (category.upper(), category))


if __name__ == "__main__":
    try:
        trip = load_trip()
        print(f"Trip: {trip.title_zh}")
        print(f"Dates: {trip.start_date} ~ {trip.end_date}")
        print(f"Days: {len(trip.days)}")
        for i, day in enumerate(trip.days):
            print(f"  Day {i + 1}: {day.date} {day.weekday_zh} {day.title_zh} ({len(day.items)} items)")
        print("\nValidation passed!")
    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        sys.exit(1)

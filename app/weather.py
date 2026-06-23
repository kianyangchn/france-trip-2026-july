"""Open-Meteo weather fetch with in-memory TTL cache."""

from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

from app.models import Trip, coords_for

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
CACHE_TTL_SECONDS = 30 * 60


@dataclass(frozen=True)
class DailyWeather:
    icon: str
    label: str
    temp_max: int
    temp_min: int


_cache: dict[tuple, tuple[float, dict[str, DailyWeather]]] = {}


# WMO weather interpretation codes → emoji + Chinese label
# https://open-meteo.com/en/docs
_WMO = {
    0: ("☀️", "晴"),
    1: ("🌤️", "晴间多云"),
    2: ("⛅", "多云"),
    3: ("☁️", "阴"),
    45: ("🌫️", "雾"),
    48: ("🌫️", "雾凇"),
    51: ("🌦️", "小毛毛雨"),
    53: ("🌦️", "毛毛雨"),
    55: ("🌧️", "大毛毛雨"),
    56: ("🌧️", "冻雨"),
    57: ("🌧️", "冻雨"),
    61: ("🌦️", "小雨"),
    63: ("🌧️", "中雨"),
    65: ("🌧️", "大雨"),
    66: ("🌧️", "冻雨"),
    67: ("🌧️", "冻雨"),
    71: ("🌨️", "小雪"),
    73: ("🌨️", "中雪"),
    75: ("❄️", "大雪"),
    77: ("❄️", "雪粒"),
    80: ("🌦️", "阵雨"),
    81: ("🌧️", "阵雨"),
    82: ("⛈️", "强阵雨"),
    85: ("🌨️", "阵雪"),
    86: ("❄️", "强阵雪"),
    95: ("⛈️", "雷暴"),
    96: ("⛈️", "雷暴冰雹"),
    99: ("⛈️", "强雷暴冰雹"),
}


def _interpret(code: int) -> tuple[str, str]:
    return _WMO.get(code, ("🌡️", "未知"))


async def _fetch_city(
    client: httpx.AsyncClient,
    lat: float,
    lon: float,
    tz: str,
    dates: list[str],
) -> dict[str, DailyWeather]:
    start, end = min(dates), max(dates)
    cache_key = (lat, lon, tz, start, end)
    now = time.time()
    cached = _cache.get(cache_key)
    if cached and now - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]

    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": tz,
        "start_date": start,
        "end_date": end,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
    }
    try:
        resp = await client.get(OPEN_METEO_URL, params=params, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
    except (httpx.HTTPError, ValueError):
        return {}

    daily = data.get("daily", {})
    times = daily.get("time", [])
    codes = daily.get("weather_code", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])

    result: dict[str, DailyWeather] = {}
    for date, code, hi, lo in zip(times, codes, tmax, tmin):
        if date not in dates:
            continue
        icon, label = _interpret(int(code))
        result[date] = DailyWeather(
            icon=icon,
            label=label,
            temp_max=round(hi),
            temp_min=round(lo),
        )

    _cache[cache_key] = (now, result)
    return result


async def get_weather_for_days(trip: Trip) -> dict[str, DailyWeather]:
    """Return {date: DailyWeather} across all days, grouped by city."""
    groups: dict[tuple[float, float, str], list[str]] = {}
    for day in trip.days:
        c = coords_for(trip, day)
        if c is None:
            continue
        key = (c.latitude, c.longitude, c.timezone)
        groups.setdefault(key, []).append(day.date)

    if not groups:
        return {}

    merged: dict[str, DailyWeather] = {}
    async with httpx.AsyncClient() as client:
        for (lat, lon, tz), dates in groups.items():
            merged.update(await _fetch_city(client, lat, lon, tz, dates))
    return merged

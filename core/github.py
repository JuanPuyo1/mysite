"""Fetch and normalize GitHub contribution calendar data."""

from __future__ import annotations

import json
import logging
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from django.conf import settings
from django.core.cache import cache

from .data import DESKTOP_CONTRIBUTION_GRID, MOBILE_CONTRIBUTION_GRID

logger = logging.getLogger(__name__)

CONTRIBUTIONS_URL = "https://github.com/users/{username}/contributions"
GRAPHQL_URL = "https://api.github.com/graphql"
USER_AGENT = "EstebanSite/1.0 (+https://github.com/JuanPuyo1)"
TD_PATTERN = re.compile(
    r'<td\b[^>]*id="contribution-day-component-(\d+)-(\d+)"[^>]*>',
    re.IGNORECASE,
)
DATE_PATTERN = re.compile(r'data-date="(\d{4}-\d{2}-\d{2})"')
LEVEL_PATTERN = re.compile(r'data-level="(\d)"')
COUNT_PATTERN = re.compile(r">(\d+) contributions? on ", re.IGNORECASE)

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 3,
}


@dataclass(frozen=True)
class ContributionData:
    total: int
    desktop_grid: list[list[int]]
    mobile_grid: list[list[int]]
    source: str
    username: str


def get_contributions() -> ContributionData:
    username = settings.GITHUB_USERNAME
    cache_key = f"github:contributions:{username}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    data = _fetch_live_contributions(username) or _fallback_contributions(username)
    cache.set(cache_key, data, timeout=settings.GITHUB_CONTRIBUTIONS_CACHE_TIMEOUT)
    return data


def _fetch_live_contributions(username: str) -> ContributionData | None:
    token = settings.GITHUB_TOKEN
    if token:
        try:
            return _fetch_graphql(username, token)
        except Exception:
            logger.exception("GitHub GraphQL contribution fetch failed for %s", username)

    try:
        return _fetch_scraped(username)
    except Exception:
        logger.exception("GitHub HTML contribution fetch failed for %s", username)
        return None


def _fetch_scraped(username: str) -> ContributionData:
    html = _http_get(CONTRIBUTIONS_URL.format(username=username))
    cells = _parse_calendar_cells(html)
    if not cells:
        raise ValueError("No contribution calendar cells found in GitHub response")

    desktop_grid = _cells_to_weeks(cells)
    mobile_grid = desktop_grid[-26:]
    total = sum(int(value) for value in COUNT_PATTERN.findall(html))
    if total == 0:
        total = sum(level > 0 for _, _, _, level in cells)

    return ContributionData(
        total=total,
        desktop_grid=desktop_grid,
        mobile_grid=mobile_grid,
        source="github",
        username=username,
    )


def _fetch_graphql(username: str, token: str) -> ContributionData:
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"username": username}}).encode()
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        body = json.load(response)

    if body.get("errors"):
        raise ValueError(body["errors"][0].get("message", "GitHub GraphQL error"))

    calendar = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    desktop_grid = [
        [LEVEL_MAP[day["contributionLevel"]] for day in week["contributionDays"]]
        for week in calendar["weeks"]
    ]

    return ContributionData(
        total=calendar["totalContributions"],
        desktop_grid=desktop_grid,
        mobile_grid=desktop_grid[-26:],
        source="github",
        username=username,
    )


def _parse_calendar_cells(html: str) -> list[tuple[int, int, str, int]]:
    cells: list[tuple[int, int, str, int]] = []
    for match in TD_PATTERN.finditer(html):
        tag = match.group(0)
        date_match = DATE_PATTERN.search(tag)
        level_match = LEVEL_PATTERN.search(tag)
        if not date_match or not level_match:
            continue
        row = int(match.group(1))
        column = int(match.group(2))
        level = min(int(level_match.group(1)), 3)
        cells.append((row, column, date_match.group(1), level))
    return cells


def _cells_to_weeks(cells: list[tuple[int, int, str, int]]) -> list[list[int]]:
    rows = max(row for row, _, _, _ in cells) + 1
    columns = max(column for _, column, _, _ in cells) + 1
    weeks: list[list[int]] = []

    for column in range(columns):
        week = [0] * rows
        for row, cell_column, _, level in cells:
            if cell_column == column:
                week[row] = level
        weeks.append(week)

    return weeks


def _http_get(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def _fallback_contributions(username: str) -> ContributionData:
    return ContributionData(
        total=1248,
        desktop_grid=DESKTOP_CONTRIBUTION_GRID,
        mobile_grid=MOBILE_CONTRIBUTION_GRID,
        source="fallback",
        username=username,
    )

"""Baixa o calendario publico de contribuicoes (sem token) e salva em data/contributions.json.

Uso: python scripts/fetch_contributions.py [usuario]
"""
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date

import requests
from bs4 import BeautifulSoup

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_USER", "joaopedro320")


def count_from_tip(text: str) -> int:
    m = re.match(r"\s*([\d,]+)\s+contribution", text or "")
    return int(m.group(1).replace(",", "")) if m else 0


def main() -> None:
    url = f"https://github.com/users/{USER}/contributions"
    r = requests.get(url, headers={"User-Agent": "profile-art-bot"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        d = td["data-date"]
        level = int(td.get("data-level", 0))
        count = count_from_tip(tips.get(td.get("id"), ""))
        days.append({"date": d, "count": count, "level": level})
    days.sort(key=lambda x: x["date"])
    if not days:
        sys.exit("nenhum dia encontrado: o HTML do GitHub mudou?")

    total = sum(x["count"] for x in days)
    head = soup.find("h2", id="js-contribution-activity-description")
    if head:
        m = re.search(r"([\d,]+)", head.get_text())
        if m:
            total = int(m.group(1).replace(",", ""))

    longest = cur = 0
    for x in days:
        cur = cur + 1 if x["count"] > 0 else 0
        longest = max(longest, cur)
    current = 0
    today = date.today().isoformat()
    for i, x in enumerate(reversed(days)):
        if x["count"] > 0:
            current += 1
        elif i == 0 and x["date"] >= today:
            continue  # hoje ainda sem commit nao zera a sequencia
        else:
            break

    best = max(days, key=lambda x: x["count"])
    monthly = defaultdict(int)
    for x in days:
        monthly[x["date"][:7]] += x["count"]

    os.makedirs("data", exist_ok=True)
    out = {
        "user": USER,
        "updated": today,
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "monthly": dict(monthly),
        "days": days,
    }
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"ok: {len(days)} dias, {total} contribuicoes, sequencia atual {current}")


if __name__ == "__main__":
    main()

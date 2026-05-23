#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from urllib.parse import quote
from urllib.request import Request, urlopen

DEV_ID = "7729187217087271065"
DEV_PAGE = f"https://play.google.com/store/apps/dev?id={DEV_ID}&hl=en&gl=us"
OUT_FILE = "data/apps.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"


def fetch_text(url: str) -> str:
  req = Request(url, headers={"User-Agent": UA})
  with urlopen(req, timeout=30) as response:
    return response.read().decode("utf-8", errors="ignore")


def parse_app_ids(dev_html: str):
  ids = re.findall(r"/store/apps/details\\?id=([A-Za-z0-9_\\.]+)", dev_html)
  return sorted(set(ids))


def parse_meta(html: str, prop: str):
  pattern = rf'<meta[^>]+property="{re.escape(prop)}"[^>]+content="([^"]*)"'
  match = re.search(pattern, html)
  return match.group(1).strip() if match else ""


def parse_description(html: str):
  # Google page often keeps short description in description meta tag.
  match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html)
  return match.group(1).strip() if match else ""


def fetch_app_data(app_id: str):
  url = f"https://play.google.com/store/apps/details?id={quote(app_id)}&hl=en&gl=us"
  html = fetch_text(url)

  title = parse_meta(html, "og:title") or app_id
  icon = parse_meta(html, "og:image")
  summary = parse_description(html)

  # Removes common Play Store suffix from title.
  title = title.replace(" - Apps on Google Play", "").strip()

  return {
    "appId": app_id,
    "title": title,
    "summary": summary,
    "icon": icon,
    "url": f"https://play.google.com/store/apps/details?id={quote(app_id)}"
  }


def main():
  dev_html = fetch_text(DEV_PAGE)
  app_ids = parse_app_ids(dev_html)

  apps = []
  for app_id in app_ids:
    try:
      apps.append(fetch_app_data(app_id))
    except Exception as err:
      print(f"Failed to fetch app {app_id}: {err}")

  payload = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "developer": {
      "id": DEV_ID,
      "url": f"https://play.google.com/store/apps/dev?id={DEV_ID}"
    },
    "apps": apps
  }

  with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

  print(f"Saved {len(apps)} app(s) to {OUT_FILE}")


if __name__ == "__main__":
  main()

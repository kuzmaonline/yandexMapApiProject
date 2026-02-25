# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
A Yandex Maps-based CRM deal geolocation dashboard. A Python backend fetches GPS data from Google Sheets, generates a JS data file, and an Nginx frontend renders objects on an interactive map. See `README.md` (in Russian) for full details.

### Development setup
- **Python venv**: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- **Env vars**: A `.env` file with `SPREADSHEET_ID` and `API_KEY` is required for the data-fetch script (`fetch_coordinates.py`). Without valid Google Sheets credentials, the script will fail with an HTTP 400 error — this is expected.
- **Existing sample data**: `static/data/coordinates.js` is committed with sample coordinate data, so the frontend map can be tested without valid API keys.

### Running services
- **Frontend dev server**: `cd static && python3 -m http.server 8080` — serves the map UI on port 8080.
- **Python data script**: `source venv/bin/activate && python fetch_coordinates.py` — fetches data from Google Sheets and writes `static/data/coordinates.js`. Requires valid `.env` credentials.
- **Docker (production)**: `docker-compose up` starts both the python-app (cron + data fetch) and nginx (port 80). Requires Docker installed.

### Key caveats
- There are no automated tests or linter configs in this repo.
- The `python3.12-venv` system package must be installed for `python3 -m venv` to work (`sudo apt-get install python3.12-venv`).
- The frontend relies on an external Yandex Maps JS API CDN (`api-maps.yandex.ru`), so internet access is needed to load the map.
- Cache file (`static/data/cache.json`) has a 1-hour TTL; delete it to force a fresh API fetch.

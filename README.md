# Power BI Auth Portal (Flask)

A minimal login portal built with Python/Flask to provide controlled access to embedded Power BI dashboards.

## Features
- Username/password login
- Session-protected dashboard route
- Per-user dashboard configuration
- Secrets loaded via `USER_DATA_JSON` or `USER_DATA_PATH`

## Config
Set env vars:
- `FLASK_SECRET_KEY`
- `USER_DATA_JSON` **or** `USER_DATA_PATH`

Example JSON:
```json
{
  "client1": {
    "password": "plain_or_hash",
    "dashboard_url": "https://app.powerbi.com/..."
  }
}

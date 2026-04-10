# ✂ SNIP — URL Shortener

A full-stack URL shortener built with **Flask + SQLite + vanilla JS**.

## Project Structure

```
url_shortener/
├── app.py              # Flask backend
├── requirements.txt
├── urls.db             # Auto-created SQLite database
└── static/
    └── index.html      # Frontend UI
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python app.py
```

Visit **http://localhost:5000** in your browser.

---

## API Endpoints

### `POST /api/shorten`
Shorten a long URL.

**Request body:**
```json
{ "url": "https://example.com/very/long/path" }
```

**Response:**
```json
{
  "short_url": "http://localhost:5000/aB3xYz",
  "code": "aB3xYz",
  "original_url": "https://example.com/very/long/path"
}
```

---

### `GET /<code>`
Redirects to the original URL and increments the click counter.

---

### `GET /api/stats`
Returns the 10 most recently created short links with click stats.

**Response:**
```json
[
  {
    "short_code": "aB3xYz",
    "original_url": "https://example.com/...",
    "clicks": 5,
    "created_at": "2024-01-15 10:30:00"
  }
]
```

---

## How It Works

1. User submits a long URL via the frontend or `POST /api/shorten`
2. Flask checks if the URL already exists in SQLite — reuses code if so
3. Otherwise, generates a random 6-character alphanumeric code
4. Stores `short_code ↔ original_url` mapping in SQLite
5. `GET /<code>` looks up the code, increments click count, and issues a `302 redirect`

## Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Python + Flask          |
| Database  | SQLite (via `sqlite3`)  |
| Frontend  | Vanilla HTML/CSS/JS     |
| Fonts     | Syne + DM Mono (Google) |

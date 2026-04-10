from flask import Flask, request, jsonify, redirect, send_from_directory
import sqlite3, string, random, os

app = Flask(__name__, static_folder='static')
DB = 'urls.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        with get_db() as conn:
            exists = conn.execute('SELECT 1 FROM urls WHERE short_code=?', (code,)).fetchone()
        if not exists:
            return code

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Check if URL already exists
    with get_db() as conn:
        existing = conn.execute('SELECT short_code FROM urls WHERE original_url=?', (url,)).fetchone()
        if existing:
            code = existing['short_code']
        else:
            code = generate_code()
            conn.execute('INSERT INTO urls (short_code, original_url) VALUES (?, ?)', (code, url))

    short_url = f"{request.host_url}{code}"
    return jsonify({'short_url': short_url, 'code': code, 'original_url': url})

@app.route('/api/stats', methods=['GET'])
def stats():
    with get_db() as conn:
        rows = conn.execute(
            'SELECT short_code, original_url, clicks, created_at FROM urls ORDER BY created_at DESC LIMIT 10'
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/<code>')
def redirect_url(code):
    with get_db() as conn:
        row = conn.execute('SELECT original_url FROM urls WHERE short_code=?', (code,)).fetchone()
        if not row:
            return jsonify({'error': 'Short URL not found'}), 404
        conn.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code=?', (code,))
    return redirect(row['original_url'], 302)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

from flask import Flask, reqeust, redirect, render_template
import sqlite3
import string
import random

app = Flask (__name__)

def generate_short_code(lenght=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(lenght))

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       original_url TEXT,
                       short_code TEXT UNIQUE)''')
    conn.commit()
    conn.close()

def get_original_url(short_code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_url(original_url, short_code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
    conn.commit()
    conn.close()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']
    short_code = generate_short_code()
    save_url(original_url, short_code)
    return f'Short URL is: {request.host}/{short_code}'

@app.route('/<short_code>')
def redirect_to_original(short_code):
    original_url = get_original_url(short_code)
    if original_url:
        return redirect(original_url)
    else:
        return 'URL not found', 404
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

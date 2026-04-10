from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
import os
from datetime import datetime
import difflib

app = Flask(__name__)

# Determine if we are running on Vercel
IS_VERCEL = os.environ.get('VERCEL') == '1'
DB_FILE = "/tmp/history.db" if IS_VERCEL else "data/history.db"

# Ensure DB exists and is initialized
def init_db():
    if not IS_VERCEL:
        os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS website_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            content TEXT NOT NULL,
            change_type TEXT,
            timestamp TEXT NOT NULL,
            specific_changes TEXT
        )
    ''')
    # Backward compatibility: Add specific_changes if missing
    try:
        c.execute('ALTER TABLE website_changes ADD COLUMN specific_changes TEXT')
    except:
        pass
    conn.commit()
    conn.close()

init_db()


def classify_change(old, new):
    diff = abs(len(new) - len(old))
    if diff < 100:
        return "Minor"
    else:
        return "Major"

def extract_specific_changes(old, new):
    old_words = old.split()
    new_words = new.split()
    diff = difflib.ndiff(old_words, new_words)
    
    added = []
    removed = []
    
    for word in diff:
        if word.startswith("+ "):
            added.append(word[2:])
        elif word.startswith("- "):
            removed.append(word[2:])
            
    res = []
    if added:
        res.append(f"Added: \"{' '.join(added)}\"")
    if removed:
        res.append(f"Removed: \"{' '.join(removed)}\"")
        
    if not res:
        return "No specific text changes detected."
    
    # Truncate if extremely long to avoid bloated DB columns
    final_string = " | ".join(res)
    if len(final_string) > 500:
        return final_string[:500] + "... (truncated)"
        
    return final_string

# Word-level diff HTML generator
def generate_diff(old, new):
    old_words = old.split()
    new_words = new.split()

    diff = difflib.ndiff(old_words, new_words)
    result = ""

    for word in diff:
        if word.startswith("+ "):
            result += f'<span class="diff-add">{word[2:]}</span> '
        elif word.startswith("- "):
            result += f'<span class="diff-remove">{word[2:]}</span> '
        else:
            result += word[2:] + " "

    return result

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    url = request.json.get("url")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        new_content = response.text[:2000]
    except Exception as e:
        return jsonify({"error": f"Failed to fetch website: {str(e)}"})

    conn = get_db_connection()
    c = conn.cursor()
    
    # Get the latest entry for this URL
    c.execute("SELECT content FROM website_changes WHERE url = ? ORDER BY id DESC LIMIT 1", (url,))
    row = c.fetchone()
    old_content = row["content"] if row else ""

    diff_html = ""
    status = ""
    change_type = ""
    specific_changes_txt = ""

    if old_content == "":
        status = "First Time Stored"
        change_type = "N/A"
        specific_changes_txt = "Initial Setup. No previous state to compare."
    elif old_content == new_content:
        status = "No Change"
        change_type = "None"
        specific_changes_txt = "No Changes."
    else:
        status = "Changed"
        change_type = classify_change(old_content, new_content)
        diff_html = generate_diff(old_content, new_content)
        specific_changes_txt = extract_specific_changes(old_content, new_content)

    # Save to database if it's the first time or if there's a change
    if status != "No Change":
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO website_changes (url, content, change_type, timestamp, specific_changes) VALUES (?, ?, ?, ?, ?)",
                  (url, new_content, change_type, current_time, specific_changes_txt))
        conn.commit()

    conn.close()

    return jsonify({
        "status": status,
        "change_type": change_type,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "diff": diff_html,
        "old": old_content,
        "new": new_content
    })

@app.route("/history")
def history():
    conn = get_db_connection()
    c = conn.cursor()
    
    # We use ROW_NUMBER() over PARTITION to compute the attempt number perfectly
    c.execute("""
        SELECT 
            id, url, change_type, timestamp, specific_changes,
            ROW_NUMBER() OVER (PARTITION BY url ORDER BY id ASC) as attempt_number
        FROM website_changes 
        ORDER BY id DESC
    """)
    records = c.fetchall()
    conn.close()
    
    # We will format this directly perfectly for the template
    formatted_data = []
    for r in records:
        raw_time = r["timestamp"]
        # raw_time is like "2026-04-09 11:47:29"
        try:
            date_part, time_part = raw_time.split(" ")
        except ValueError:
            date_part = raw_time
            time_part = "00:00:00"
            
        formatted_data.append({
            "url": r["url"],
            "attempt": r["attempt_number"],
            "date": date_part,
            "time": time_part,
            "specific_changes": r["specific_changes"] if r["specific_changes"] else "No granular details recorded."
        })
    
    return render_template("history.html", records=formatted_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
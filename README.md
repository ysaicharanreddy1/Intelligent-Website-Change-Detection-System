# Intelligent Website Change Detection System

This project is an intelligent, automated website change detection system. It allows users to continuously monitor any URL, fetching its latest content and automatically detecting modifications. So, basically we give the website URL. It shows the previous version and the new changed version after any changes are made in that particular website. It also stores the changes which are done in that website.


## Tech Stack

* **Backend**: Python 3, Flask, built-in libraries (`requests`, `sqlite3`, `difflib`)
* **Frontend**: JavaScript, HTML, CSS 
* **Database**: SQLite (persisted in `/data/history.db`)


## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Intelligent-Website-Change-Detection-System.git
   cd Intelligent-Website-Change-Detection-System
   ```

2. **Set up a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   The primary dependencies for this project are Flask and Requests.
   ```bash
   pip install Flask requests
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   The server will start on `http://127.0.0.1:5000/`.

## Usage Instructions

1. Open your browser and navigate to `http://127.0.0.1:5000/`.
2. Open new terminal and then type under test.html "python -m http.server 8000" and then open `http://127.0.0.1:8000/test.html`. Now, come back to VS code and     make changes in test.html and view the website monitoring webpage, what happens in the project. 
3. Click **Check Now** to perform a one-time scrape and difference check.
4. Click **Start Polling** to continuously monitor the target URL. 
5. To view previously captured changes, click the **History** button. You can browse through different snapshots and see specific granular text deviations!

## 📁 Project Structure

```
WebPulse-Monitor/
│
├── app.py                  
├── data/
│   └── history.db          # Auto-generated SQLite database
├── static/
│   ├── style.css           
│   └── script.js           
├── templates/
│   ├── index.html          
│   └── history.html        
├── .gitignore              # Ignored files (e.g., venv, pycache, history.db)
└── README.md               
```
## Deployed on vercel app

Link : `https://website-monitor-cis.vercel.app/`

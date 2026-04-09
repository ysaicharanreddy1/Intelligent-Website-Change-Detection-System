# WebPulse Monitor (Intelligent Website Change Detection System)

![WebPulse Monitor](https://img.shields.io/badge/Status-Active-success)
![Python Version](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)

**WebPulse Monitor** is an intelligent, automated website change detection system. It allows users to continuously monitor any URL, fetching its latest content and automatically detecting modifications. Built with a robust **Flask API backend** and a modern, aesthetically pleasing frontend, this tool features accurate change classification, visual word-level diff tracking, and persistent history tracking.

## 🚀 Key Features

* **Automated & Manual Polling**: Start an automated polling loop or manually trigger checks whenever you need.
* **Intelligent Change Classification**: Automatically classifies changes as **Minor** or **Major** based on content modification thresholds.
* **Word-Level Diff Visualization**: See exactly what changed! Added text is highlighted in green, and removed text is highlighted in red, allowing for quick visual analysis.
* **Persistent History Tracking**: Uses a SQLite database to track every attempt, capturing timestamps, specific text changes, and difference reports for later review.
* **Dual Interface View**: Side-by-side splitting clearly illustrates the 'Previous State' vs 'Current State' of the targeted URL.
* **Modern & Responsive UI**: Glassmorphism design elements alongside clean dashboard status cards make user experience seamless and elegant.

## 🛠️ Tech Stack

* **Backend**: Python 3, Flask, built-in libraries (`requests`, `sqlite3`, `difflib`)
* **Frontend**: Vanilla JavaScript (ES6), HTML5, CSS3 
* **Database**: SQLite (persisted in `/data/history.db`)
* **Fonts**: Google Fonts (Inter)

## 📋 Prerequisites

Ensure you have Python installed on your local machine. You will also need `pip` for package management.

* [Python 3.7+](https://www.python.org/downloads/)

## ⚙️ Installation & Setup

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

## 💻 Usage Instructions

1. Open your browser and navigate to `http://127.0.0.1:5000/`.
2. Enter the absolute URL of the website you want to monitor (e.g., `https://example.com`) into the input field.
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

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check [issues page](https://github.com/yourusername/Intelligent-Website-Change-Detection-System/issues) if you want to contribute.

# Mini Search Engine - Vaksin Campak

Aplikasi search engine mini menggunakan TF-IDF untuk mencari dokumen berdasarkan query dari dataset vaksin campak.

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/dzraka/mini-search-engine.git
cd mini-search-engine
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**CMD:**

```bash
venv\Scripts\activate
```

**Git Bash:**

```bash
source venv/Scripts/activate
# or
. venv/Scripts/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Buka browser dan akses: http://localhost:5000

## Project Structure

```bash
.
├── app.py                      # Flask main application
├── search_engine.py            # TF-IDF search implementation
├── vaksin_campak.csv           # Dataset komentar vaksin campak
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── notebook/
│   └── vaksin_campak.ipynb     # Jupyter notebook
├── static/
│   ├── style.css               # CSS styling
│   └── script.js               # JavaScript frontend
└── templates/
    └── index.html              # HTML template
```

## Dependencies

- **Flask** (3.1.3) - Web framework
- **Pandas** (3.0.3) - Data processing dan manipulation
- **NumPy** (2.4.6) - Numerical computations
- **Sastrawi** (1.0.1) - Indonesian text processing (stemming & stopwords)
- **Python 3.8+**

Lihat `requirements.txt` untuk versi lengkap semua dependencies.

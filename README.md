# EcoTrack - Environmental Reporting & Animal Sightings Platform

A web app for reporting environmental issues and wildlife sightings in Batangas Province.

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/EthanSapuay222/sql-database-project.git
cd sql-database-project
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask
- Flask-SQLAlchemy
- Flask-Cors
- Flask-WTF
- WTForms
- Werkzeug

**That's it!** The app uses SQLite by default (no database setup needed).

### Step 4: Load Sample Data
```bash
python seed.py
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Open in Browser
Go to `http://localhost:5000`

**Default Login:**
- Username: `admin`
- Password: `admin`

## Troubleshooting

**Virtual environment won't activate?**
- Make sure you're in the project directory
- Try: `python -m venv venv` first
- Then run the activate command again

**pip install fails?**
- Make sure virtual environment is activated (you should see `(venv)` in your terminal)
- Try: `pip install --upgrade pip`
- Then run `pip install -r requirements.txt` again

**Can't connect to database?**
- Make sure PostgreSQL is running and installed
- Check that `.env` has the correct username and password
- Verify the database name exists

**Port 5000 already in use?**
- Open `app.py` and change the last line:
  ```python
  app.run(port=5001)  # Change 5000 to 5001
  ```

**Need to reset the database?**
- Delete the database in PostgreSQL
- Run `python seed.py` again

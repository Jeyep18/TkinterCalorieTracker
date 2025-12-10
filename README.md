# TkinterCalorieTracker

A modern calorie tracking desktop application built with Python, CustomTkinter, and MySQL.

## Features

- **Profile Setup**: Create your profile with personal stats to calculate your daily calorie goal
- **Search Foods**: Search the food database and log meals with serving sizes
- **Add Custom Foods**: Add your own foods with nutritional information
- **Daily Log**: View all foods logged today, grouped by meal type
- **Progress Tracking**: Visual progress bar showing daily calorie consumption

## Prerequisites

- **Python 3.8+**
- **MySQL Server** (running locally or remotely)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Jeyep18/TkinterCalorieTracker.git
cd TkinterCalorieTracker
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a `.env` file in the project root with your MySQL credentials:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=calorie_tracker
```

> **Note**: Create the `calorie_tracker` database in MySQL before running the app:
> ```sql
> CREATE DATABASE calorie_tracker;
> ```

### 5. Run the Application

```bash
python main.py
```

## Project Structure

```
TkinterCalorieTracker/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Database credentials (create this)
├── config/
│   └── database.py
├── database/
│   ├── db_manager.py       # Database connection manager
│   └── schema.sql          # Database schema
├── gui/
│   ├── main_window.py      # Main dashboard
│   ├── profile_setup.py    # Profile creation screen
│   ├── food_search.py      # Food search dialog
│   ├── add_food.py         # Add custom food dialog
│   └── daily_log.py        # Daily food log viewer
├── models/
│   ├── user.py             # User model
│   ├── food.py             # Food model
│   └── food_log.py         # Food log model
└── services/
    ├── calorie_calculator.py   # BMR/TDEE calculations
    └── daily_reset_service.py  # Daily log management
```

## Usage

1. **First Launch**: Create your profile by entering your stats (age, weight, height, activity level, goal)
2. **Search Food**: Click "Search Food" to find and log foods from the database
3. **Add Custom Food**: Click "Add Custom Food" to add your own foods
4. **View Daily Log**: Click "View Today's Log" to see all logged foods grouped by meal

## Dependencies

- `customtkinter` - Modern UI widgets
- `mysql-connector-python` - MySQL database connection
- `python-dotenv` - Environment variable management
- `pillow` - Image processing
- `requests` - HTTP requests

## License

This project is part of an OOP Finals Project.

# team_manager/app/models.py
import sqlite3

DB_NAME = "app/team_manager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Employees
    c.execute("""
    CREATE TABLE IF NOT EXISTS Employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # Surveys
    c.execute("""
    CREATE TABLE IF NOT EXISTS Surveys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        avg_bill TEXT,
        target_reached TEXT,
        shelf_bar_sales TEXT,
        actions_done TEXT,
        development_goals TEXT,
        new_products_sales TEXT,
        foreign_orders TEXT,
        costs_summary TEXT,
        losses_summary TEXT,
        promo_sales TEXT,
        team_status TEXT,
        meetings_done TEXT,
        staffing_needs TEXT,
        external_integrators TEXT,
        general_topics TEXT,
        week_date TEXT,
        FOREIGN KEY(employee_id) REFERENCES Employees(id)
    )
    """)

    # Tasks
    c.execute("""
    CREATE TABLE IF NOT EXISTS Tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        task TEXT,
        done INTEGER DEFAULT 0,
        FOREIGN KEY(employee_id) REFERENCES Employees(id)
    )
    """)

    conn.commit()
    conn.close()

# Uruchomienie inicjalizacji bazy przy starcie
init_db()

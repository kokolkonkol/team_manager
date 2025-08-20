# team_manager/app/crud.py
import sqlite3
from app.models import DB_NAME
from app.schemas import SurveyCreate
from sqlite3 import Error
from contextlib import contextmanager
from typing import Generator
import threading
import os
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    _lock = threading.Lock()
    _local = threading.local()

    def __init__(self, db_path: str = None):
        if db_path is None:
            # Always use survey.db from data directory
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'data', 
                'survey.db'
            )
        self.db_path = db_path

    def get_connection(self):
        if not hasattr(self._local, 'connection'):
            with self._lock:
                self._local.connection = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False
                )
                self._local.connection.row_factory = sqlite3.Row
        return self._local.connection

    def cursor(self):
        return self.get_connection().cursor()

    def commit(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.commit()

    def close(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection

def get_db() -> Generator[DatabaseConnection, None, None]:
    db = DatabaseConnection()
    try:
        yield db
    finally:
        db.close()

# --- Employees ---
def get_all_employees():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM Employees")
    data = [{"id": row[0], "name": row[1]} for row in c.fetchall()]
    conn.close()
    return data

def get_employee(employee_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM Employees WHERE id = ?", (employee_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1]}
    return None

def create_employee(name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO Employees (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def update_employee(employee_id: int, name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE Employees SET name = ? WHERE id = ?", (name, employee_id))
    conn.commit()
    conn.close()

def delete_employee(employee_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM Employees WHERE id = ?", (employee_id,))
    conn.commit()
    conn.close()

def get_employees():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM employees")
        return c.fetchall()
    finally:
        conn.close()

# --- Surveys ---
def get_latest_surveys():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM Surveys ORDER BY week_date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def create_survey(employee_id: int, survey: SurveyCreate):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO Surveys (
        employee_id, avg_bill, target_reached, shelf_bar_sales,
        actions_done, development_goals, new_products_sales,
        foreign_orders, costs_summary, losses_summary, promo_sales,
        team_status, meetings_done, staffing_needs, external_integrators,
        general_topics, week_date
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        employee_id, survey.avg_bill, survey.target_reached, survey.shelf_bar_sales,
        survey.actions_done, survey.development_goals, survey.new_products_sales,
        survey.foreign_orders, survey.costs_summary, survey.losses_summary, survey.promo_sales,
        survey.team_status, survey.meetings_done, survey.staffing_needs, survey.external_integrators,
        survey.general_topics, str(survey.week_date)
    ))
    conn.commit()
    conn.close()

def save_survey(data: dict) -> bool:
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO surveys (
                    employee_id, manager_name, week_date,
                    avg_bill, target_reached, team_status
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['employee_id'], 
                data['manager_name'],
                data['week_date'],
                data['avg_bill'],
                data['target_reached'],
                data['team_status']
            ))
            return True
    except Error as e:
        print(f"Database error: {e}")
        return False

# --- Tasks ---
def get_tasks():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, employee_id, task, done FROM Tasks")
    tasks = [{"id": r[0], "employee_id": r[1], "task": r[2], "done": bool(r[3])} for r in c.fetchall()]
    conn.close()
    return tasks

# --- Recommendations ---
def get_recommendations(employee_id: int):
    return [
        "Przeprowadź dodatkowe szkolenie baristów",
        "Zaktualizuj plakaty promocyjne na półce",
        "Omów wyniki sprzedaży w kolejnym 1on1"
    ]

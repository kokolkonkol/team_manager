from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .crud import get_db, DatabaseConnection
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: DatabaseConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM employees")
    employees = [dict(row) for row in cursor.fetchall()]
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "employees": employees}
    )

@app.get("/employees", response_class=HTMLResponse)
async def employee_management(request: Request, db: DatabaseConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM employees")
    employees = [dict(row) for row in cursor.fetchall()]
    return templates.TemplateResponse(
        "employee_management.html",
        {"request": request, "employees": employees}
    )

@app.post("/employee", response_class=RedirectResponse)
async def create_employee(name: str = Form(...), db: DatabaseConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO employees (name) VALUES (?)", (name,))
    db.commit()
    return RedirectResponse("/employees", status_code=303)

@app.post("/employee/{employee_id}/delete")
async def delete_employee(employee_id: int, db: DatabaseConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    db.commit()
    return RedirectResponse("/employees", status_code=303)

@app.get("/surveys", response_class=HTMLResponse)
async def surveys_list(request: Request, db: DatabaseConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT s.*, e.name as employee_name 
        FROM surveys s 
        LEFT JOIN employees e ON s.employee_id = e.id 
        ORDER BY s.created_at DESC
    """)
    surveys = [dict(row) for row in cursor.fetchall()]
    return templates.TemplateResponse(
        "surveys.html",
        {"request": request, "surveys": surveys}
    )

@app.get("/survey/{employee_id}", response_class=HTMLResponse)
async def new_survey_form(employee_id: int, request: Request, db: DatabaseConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM employees WHERE id = ?", (employee_id,))
    employee = cursor.fetchone()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return templates.TemplateResponse(
        "survey_form.html",
        {"request": request, "employee": dict(employee)}
    )

@app.get("/survey/{survey_id}/details", response_class=HTMLResponse)
async def survey_details(survey_id: int, request: Request, db: DatabaseConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT s.*, e.name as employee_name 
        FROM surveys s 
        LEFT JOIN employees e ON s.employee_id = e.id 
        WHERE s.id = ?
    """, (survey_id,))
    survey = cursor.fetchone()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return templates.TemplateResponse(
        "survey_details.html",
        {"request": request, "survey": dict(survey)}
    )

@app.post("/survey")
async def create_survey(
    request: Request,
    db: DatabaseConnection = Depends(get_db),
    manager_name: str = Form(...),
    employee_id: int = Form(...),
    week_date: str = Form(...),
    avg_bill: str = Form(...),
    target_reached: str = Form(...),
    shelf_bar_sales: str = Form(...),
    actions_done: str = Form(...),
    development_goals: str = Form(...),
    foreign_orders: str = Form(...),
    new_products_sales: str = Form(...),
    salary_costs: str = Form(None),  # Changed from costs_summary
    losses_analysis: str = Form(None),  # Changed from losses_summary
    promo_sales: str = Form(...),
    team_status: str = Form(...),
    weekly_meetings: str = Form(None),  # Changed from meetings_done
    staffing_needs: str = Form(...),
    delivery_integrators: str = Form(...),  # Changed from external_integrators
    general_topics: str = Form(...)
):
    """Create new survey"""
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO surveys (
            manager_name, employee_id, week_date, avg_bill, target_reached,
            shelf_bar_sales, actions_done, development_goals, foreign_orders,
            new_products_sales, costs_summary, losses_summary, promo_sales,
            team_status, meetings_done, staffing_needs, external_integrators,
            general_topics
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        manager_name, employee_id, week_date, avg_bill, target_reached,
        shelf_bar_sales, actions_done, development_goals, foreign_orders,
        new_products_sales, salary_costs, losses_analysis, promo_sales,
        team_status, weekly_meetings, staffing_needs, delivery_integrators,
        general_topics
    ))
    db.commit()
    return RedirectResponse("/surveys", status_code=303)
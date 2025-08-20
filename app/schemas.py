# team_manager/app/schemas.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class SurveyCreate(BaseModel):
    employee_id: int
    manager_name: str = Field(..., min_length=2)
    week_date: date
    avg_bill: Optional[str]
    target_reached: Optional[str]
    team_status: Optional[str]

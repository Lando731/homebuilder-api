from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

MATERIAL_COSTS = {
    "framing": 15.0,
    "drywall": 2.0,
    "roofing": 5.0,
    "flooring": 4.0,
    "windows": 300.0,
    "doors": 150.0
}

LABOR_COSTS = {
    "site_prep": 3000,
    "foundation": 8000,
    "framing": 7000,
    "roofing": 5000,
    "windows_doors": 2500,
    "rough_ins": 6000,
    "drywall": 4000,
    "flooring": 3500,
    "finishes": 3000,
    "inspection": 1000
}

TASK_DURATIONS = {
    "Site Prep": 3,
    "Foundation": 5,
    "Framing": 7,
    "Roofing": 4,
    "Windows & Doors": 3,
    "Electrical & Plumbing Rough-in": 6,
    "Drywall & Insulation": 5,
    "Flooring & Interior Trim": 4,
    "Paint & Fixtures": 3,
    "Final Inspection": 2
}

class PlanInput(BaseModel):
    square_footage: int
    bedrooms: int
    bathrooms: int
    windows: int
    doors: int

class EstimateOutput(BaseModel):
    materials: Dict[str, float]
    labor: Dict[str, float]
    total_cost: float
    schedule: List[str]

@app.post("/estimate", response_model=EstimateOutput)
def estimate_plan(data: PlanInput):
    materials = {
        "framing": data.square_footage * MATERIAL_COSTS["framing"],
        "drywall": data.square_footage * MATERIAL_COSTS["drywall"],
        "roofing": data.square_footage * MATERIAL_COSTS["roofing"],
        "flooring": data.square_footage * MATERIAL_COSTS["flooring"],
        "windows": data.windows * MATERIAL_COSTS["windows"],
        "doors": data.doors * MATERIAL_COSTS["doors"],
    }

    labor = LABOR_COSTS.copy()

    total = sum(materials.values()) + sum(labor.values())

    schedule = []
    day_counter = 1
    for task, duration in TASK_DURATIONS.items():
        start_day = day_counter
        end_day = start_day + duration - 1
        schedule.append(f"{task} (Day {start_day}-{end_day})")
        day_counter = end_day + 1

    return EstimateOutput(materials=materials, labor=labor, total_cost=total, schedule=schedule)

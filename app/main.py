from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


class Country(BaseModel):
    name: str
    code: str
    capital: str
    region: str


COUNTRIES = [
    Country(name="Australia", code="AU", capital="Canberra", region="Oceania"),
    Country(name="Brazil", code="BR", capital="Brasilia", region="South America"),
    Country(name="Canada", code="CA", capital="Ottawa", region="North America"),
    Country(name="France", code="FR", capital="Paris", region="Europe"),
    Country(name="India", code="IN", capital="New Delhi", region="Asia"),
    Country(name="Japan", code="JP", capital="Tokyo", region="Asia"),
    Country(name="Kenya", code="KE", capital="Nairobi", region="Africa"),
    Country(name="United States", code="US", capital="Washington, D.C.", region="North America"),
]


class Employee(BaseModel):
    id: int
    name: str
    role: str
    department: str
    email: str
    location: str


class EmployeeCreate(BaseModel):
    name: str
    role: str
    department: str
    email: str
    location: str


# In-memory storage
EMPLOYEES: List[Employee] = [
    Employee(id=1, name="Alice Johnson", role="Software Engineer", department="Engineering", email="alice.johnson@example.com", location="New York"),
    Employee(id=2, name="Bob Lee", role="Product Manager", department="Product", email="bob.lee@example.com", location="San Francisco"),
    Employee(id=3, name="Carla Gomez", role="Data Scientist", department="Data", email="carla.gomez@example.com", location="Austin"),
    Employee(id=4, name="Daniel Kim", role="UX Designer", department="Design", email="daniel.kim@example.com", location="Seattle"),
]
_next_employee_id = max(e.id for e in EMPLOYEES) + 1 if EMPLOYEES else 1


app = FastAPI(title="Countries & Employees API", version="1.0.0")


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"message": "Countries & Employees API is running"}


@app.get("/countries", response_model=List[Country], tags=["countries"]) 
def list_countries() -> List[Country]:
    return COUNTRIES


@app.get("/employees", response_model=List[Employee], tags=["employees"]) 
def list_employees() -> List[Employee]:
    return EMPLOYEES


@app.post("/employees", response_model=Employee, tags=["employees"], status_code=201)
def create_employee(employee: EmployeeCreate) -> Employee:
    global _next_employee_id
    new_employee = Employee(id=_next_employee_id, **employee.dict())
    _next_employee_id += 1
    EMPLOYEES.append(new_employee)
    return new_employee


@app.get("/employees/{employee_id}", response_model=Employee, tags=["employees"]) 
def get_employee(employee_id: int) -> Employee:
    for emp in EMPLOYEES:
        if emp.id == employee_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.put("/employees/{employee_id}", response_model=Employee, tags=["employees"]) 
def update_employee(employee_id: int, employee: EmployeeCreate) -> Employee:
    for idx, emp in enumerate(EMPLOYEES):
        if emp.id == employee_id:
            updated = Employee(id=employee_id, **employee.dict())
            EMPLOYEES[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/employees/{employee_id}", tags=["employees"], status_code=200)
def delete_employee(employee_id: int) -> dict:
    for idx, emp in enumerate(EMPLOYEES):
        if emp.id == employee_id:
            EMPLOYEES.pop(idx)
            return {"detail": "Employee deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")

from fastapi import FastAPI
from pydantic import BaseModel


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


EMPLOYEES = [
    Employee(id=1, name="Alice Johnson", role="Software Engineer", department="Engineering", email="alice.johnson@example.com", location="New York"),
    Employee(id=2, name="Bob Lee", role="Product Manager", department="Product", email="bob.lee@example.com", location="San Francisco"),
    Employee(id=3, name="Carla Gomez", role="Data Scientist", department="Data", email="carla.gomez@example.com", location="Austin"),
    Employee(id=4, name="Daniel Kim", role="UX Designer", department="Design", email="daniel.kim@example.com", location="Seattle"),
]


app = FastAPI(title="Countries & Employees API", version="1.0.0")


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"message": "Countries & Employees API is running"}


@app.get("/countries", response_model=list[Country], tags=["countries"]) 
def list_countries() -> list[Country]:
    return COUNTRIES


@app.get("/employees", response_model=list[Employee], tags=["employees"]) 
def list_employees() -> list[Employee]:
    return EMPLOYEES

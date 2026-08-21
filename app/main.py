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

app = FastAPI(title="Countries API", version="1.0.0")


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"message": "Countries API is running"}


@app.get("/countries", response_model=list[Country], tags=["countries"])
def list_countries() -> list[Country]:
    return COUNTRIES

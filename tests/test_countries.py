from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_countries_returns_country_data() -> None:
    response = client.get("/countries")

    assert response.status_code == 200
    countries = response.json()
    assert len(countries) == 8
    assert countries[0] == {
        "name": "Australia",
        "code": "AU",
        "capital": "Canberra",
        "region": "Oceania",
    }


def test_openapi_documents_countries_endpoint() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/countries" in response.json()["paths"]

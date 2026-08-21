# Countries API

A small Python project built with [FastAPI](https://fastapi.tiangolo.com/) that exposes country data as JSON. The API currently stores eight countries in memory and provides automatic interactive documentation through OpenAPI.

## What This Project Does

The application provides three useful URLs:

| Method | URL | Purpose |
| --- | --- | --- |
| `GET` | `/` | Returns a simple health message to confirm that the API is running. |
| `GET` | `/countries` | Returns the complete list of countries. |
| `GET` | `/docs` | Opens FastAPI's interactive Swagger UI documentation. |

The country response contains four fields:

```json
{
	"name": "Australia",
	"code": "AU",
	"capital": "Canberra",
	"region": "Oceania"
}
```

## Project Structure

```text
.
|-- app/
|   |-- __init__.py       # Marks app as a Python package
|   `-- main.py           # FastAPI application, model, data, and routes
|-- tests/
|   |-- __init__.py       # Marks tests as a Python package
|   `-- test_countries.py  # Endpoint and OpenAPI tests
|-- .gitignore             # Files excluded from source control
|-- pyproject.toml         # Pytest configuration
|-- requirements.txt       # Runtime and test dependencies
`-- README.md              # Project documentation
```

## Requirements

- Python 3.10 or newer. The project uses built-in generic type syntax such as `list[Country]`.
- PowerShell, Command Prompt, or another terminal.
- Internet access during installation so pip can download dependencies.

## Installation

Open a terminal in the project directory and create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current user, run this once in an administrator-approved shell or follow your organization's Python setup policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Using `python -m pip` ensures that packages are installed into the same Python environment used to run the project.

## Dependencies

The dependencies are declared in `requirements.txt`:

- `fastapi` provides the web framework, routing, request handling, validation, and OpenAPI generation.
- `uvicorn[standard]` runs the FastAPI application as an ASGI server and enables reload support during development.
- `pytest` runs the automated tests.
- `httpx` is used by FastAPI's `TestClient` to make in-process HTTP requests in the tests.

## Application Walkthrough

The application is defined in `app/main.py`.

### 1. Define the response model

The `Country` Pydantic model describes the shape of every country:

```python
class Country(BaseModel):
		name: str
		code: str
		capital: str
		region: str
```

FastAPI uses this model to validate the data and generate the schema shown in the API documentation.

### 2. Store the country data

`COUNTRIES` is a Python list containing `Country` objects. It is an in-memory data source, which keeps the example easy to understand. Data will reset whenever the application restarts, so a production application would normally replace this list with a database or external service.

### 3. Create the FastAPI application

```python
app = FastAPI(title="Countries API", version="1.0.0")
```

The `app` object is the ASGI application that Uvicorn loads. The title and version appear in the generated OpenAPI document and Swagger UI.

### 4. Add the routes

The root route returns a health message. The countries route returns the list and declares `list[Country]` as its response model:

```python
@app.get("/countries", response_model=list[Country], tags=["countries"])
def list_countries() -> list[Country]:
		return COUNTRIES
```

The response model means clients receive a predictable JSON array and the endpoint is documented automatically.

## Run the API

With the virtual environment activated, start the development server:

```powershell
uvicorn app.main:app --reload
```

The command follows the format `uvicorn module:object`. In this project, `app.main` points to `app/main.py` and `app` is the FastAPI instance inside that module.

The server is available at:

- API root: <http://127.0.0.1:8000/>
- Country list: <http://127.0.0.1:8000/countries>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

The `--reload` option watches the source files and restarts the server after code changes. It is intended for development, not production.

To stop the server, press `Ctrl+C`.

## Example Response

Request:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/countries
```

Response:

```json
[
	{
		"name": "Australia",
		"code": "AU",
		"capital": "Canberra",
		"region": "Oceania"
	},
	{
		"name": "Brazil",
		"code": "BR",
		"capital": "Brasilia",
		"region": "South America"
	}
]
```

The actual response includes all eight countries defined in `COUNTRIES`.

## Run the Tests

Run all tests from the project root:

```powershell
python -m pytest
```

The tests in `tests/test_countries.py` verify that:

1. `GET /countries` returns HTTP `200`.
2. The response contains the expected eight countries.
3. The first country has the expected fields and values.
4. `/countries` is included in the generated OpenAPI schema.

## How to Add a Country

Add another `Country` object to the `COUNTRIES` list in `app/main.py`:

```python
Country(name="Germany", code="DE", capital="Berlin", region="Europe"),
```

Then run the tests again. If the list length is intentionally changed, update the corresponding assertion in `tests/test_countries.py`.

## How to Extend the API

Natural next steps include:

- Add `GET /countries/{code}` to return one country by its two-letter code.
- Add query parameters such as `?region=Europe` for filtering.
- Move country data into a database or JSON file.
- Add pagination when the dataset becomes large.
- Add stricter validation for country codes, such as exactly two uppercase letters.
- Add CORS configuration if a browser frontend will call the API from another origin.
- Add logging, authentication, and deployment configuration for production use.

## Troubleshooting

### `uvicorn` is not recognized

Run it through the active Python environment instead:

```powershell
python -m uvicorn app.main:app --reload
```

### `ModuleNotFoundError` when running tests

Confirm that the virtual environment is activated and reinstall the dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

### Port 8000 is already in use

Start the server on another port:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

Then use `http://127.0.0.1:8001/` for the API.

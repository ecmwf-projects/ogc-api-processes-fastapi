from fastapi.testclient import TestClient

from ogc_api_processes_fastapi.main import app

client = TestClient(app)


def test_get_process_list():
    response = client.get("/processes")
    assert response.status_code == 200
    assert response.json() == {
        "processes": [
            {"id": "retrieve-era5-single-levels", "version": "0.1"},
            {"id": "retrieve-era5-pressure-levels", "version": "0.1"},
            {"id": "retrieve-era5-land", "version": "0.1"},
        ],
        "links": [{"href": "http://127.0.0.1:8000/processes/", "rel": "self"}],
    }

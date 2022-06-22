from fastapi.testclient import TestClient

from ogc_api_processes_fastapi.main import app

client = TestClient(app)


def test_get_process_list() -> None:
    response = client.get("/processes")
    assert response.status_code == 200
    assert response.json() == {
        "processes": [
            {"id": "retrieve-reanalysis-era5-single-levels", "version": "0.1"},
            {"id": "retrieve-reanalysis-era5-pressure-levels", "version": "0.1"},
            {"id": "retrieve-reanalysis-era5-land", "version": "0.1"},
            {"id": "retrieve-reanalysis-era5-land-monthly-means", "version": "0.1"},
        ],
        "links": [{"href": "http://testserver/processes", "rel": "self"}],
    }


def test_get_process_list_limit() -> None:
    response = client.get("/processes?limit=1")
    assert response.status_code == 200
    assert response.json() == {
        "processes": [
            {"id": "retrieve-reanalysis-era5-single-levels", "version": "0.1"},
        ],
        "links": [{"href": "http://testserver/processes", "rel": "self"}],
    }

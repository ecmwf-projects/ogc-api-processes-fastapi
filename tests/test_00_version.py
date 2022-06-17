import ogc_api_processes_fastapi


def test_version() -> None:
    assert ogc_api_processes_fastapi.__version__ != "999"

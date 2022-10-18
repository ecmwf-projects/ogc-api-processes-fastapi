import pydantic

import ogc_api_processes_fastapi.responses


def test_generate_schema_default():
    schema = ogc_api_processes_fastapi.responses.generate_schema()

    exp_keys = [
        "Metadata",
        "AdditionalParameter",
        "Link",
        "ConfClass",
        "AdditionalParameters",
        "DescriptionType",
        "ProcessSummary",
        "ProcessesList",
        "Reference",
        "SchemaItem",
        "InputDescription",
        "OutputDescription",
        "Bbox",
        "InputValueNoObject",
        "Format",
        "inputValue",
        "QualifiedInputValue",
        "InlineOrRefData",
        "Output",
        "Subscriber",
        "Execute",
        "ProcessDescription",
        "StatusInfo",
        "JobList",
        "Results",
        "Exception",
        "LandingPage",
    ]
    schema_keys = list(schema.keys())
    assert schema_keys == exp_keys

    exp_type = pydantic.main.ModelMetaclass
    for key in schema_keys:
        schema_type = type(schema[key])
        assert schema_type == exp_type


def test_generate_schema_add_params():

    schema_default = ogc_api_processes_fastapi.responses.generate_schema()
    test_model_name = "StatusInfo"
    test_model = schema_default[test_model_name]
    assert "metadata" not in test_model.__fields__.keys()

    additional_parameters = {test_model_name: {"metadata": (str, ...)}}
    schema = ogc_api_processes_fastapi.responses.generate_schema(additional_parameters)
    test_model = schema[test_model_name]
    assert "metadata" in test_model.__fields__.keys()

    exp_add_field_name = "metadata"
    exp_add_field_type = str
    exp_add_field_required = True
    add_field_name = test_model.__fields__["metadata"].name
    add_field_type = test_model.__fields__["metadata"].type_
    add_field_required = test_model.__fields__["metadata"].required
    assert add_field_name == exp_add_field_name
    assert add_field_type == exp_add_field_type
    assert add_field_required == exp_add_field_required

    test_inheriting_model_name = "JobList"
    test_inheriting_model = schema[test_inheriting_model_name]
    exp_field = "jobs"
    fields = test_inheriting_model.__fields__
    assert exp_field in fields.keys()
    assert exp_add_field_name in fields["jobs"].type_.__fields__.keys()

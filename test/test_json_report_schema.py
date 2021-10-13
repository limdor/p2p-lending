import os
import json
import jsonschema
import pytest


def test_jsonschema_version():
    assert jsonschema.__version__ == "3.2.0"


def test_location_monthly_report_schema():
    assert os.path.exists("schemas/monthlyReport.json")


def test_monthly_report_schema_is_valid_json():
    with open("schemas/monthlyReport.json", encoding='utf-8', errors='strict') as json_file:
        assert json.load(json_file)


def test_schema_validation_does_not_allow_additional_properties():
    with open("schemas/monthlyReport.json", encoding='utf-8', errors='strict') as json_file:
        schema = json.load(json_file)
        instance = {"undefinedProperty": "value"}
        with pytest.raises(jsonschema.exceptions.ValidationError) as validation_error:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(validation_error.value)

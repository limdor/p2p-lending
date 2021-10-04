import os
import json
import jsonschema


def test_jsonschema_version():
    assert jsonschema.__version__ == "3.2.0"


def test_location_monthly_report_schema():
    assert os.path.exists("schemas/monthlyReport.json")


def test_monthly_report_schema_is_valid_json():
    with open("schemas/monthlyReport.json", encoding='utf-8', errors='strict') as json_file:
        assert json.load(json_file)

import sys
import datetime
import jsonschema
import pytest


def test_jsonschema_version():
    assert "3.2.0" == jsonschema.__version__

if __name__ == "__main__":
    sys.exit(pytest.main(["-rA",__file__]))

import pytest
from pydantic import ValidationError
from src.models import ExtractionResult, ModuleStructure

def test_valid_structure():
    data = {
        "module": "Account",
        "Description": "Settings for accounts",
        "Submodules": {"Login": "How to login"}
    }
    model = ModuleStructure(**data)
    assert model.module == "Account"
    assert model.description == "Settings for accounts"

def test_invalid_structure_missing_field():
    data = {
        "module": "Account",
        # Missing Description
        "Submodules": {}
    }
    with pytest.raises(ValidationError):
        ModuleStructure(**data)

def test_extraction_result_list():
    data = {
        "hierarchy": [
            {
                "module": "A",
                "Description": "Desc A",
                "Submodules": {"Sub A": "Desc Sub A"}
            }
        ]
    }
    result = ExtractionResult(**data)
    assert len(result.hierarchy) == 1
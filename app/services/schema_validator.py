from fastapi import HTTPException
from datetime import datetime
from typing import Any, Dict

class SchemaValidator:
    """
    Enforces payload integrity against dynamically defined project resources.
    Simulates Firebase Firestore strict schema mode rules.
    """
    @staticmethod
    def validate_payload(schema: Dict[str, str], payload: Dict[str, Any]) -> None:
        if not schema:
            return  # Schema-less dynamic mode, accept any dictionary
            
        for field, expected_type in schema.items():
            if field not in payload:
                raise HTTPException(status_code=400, detail=f"Missing required field: '{field}'")
                
            value = payload[field]
            try:
                if expected_type.lower() == "string" and not isinstance(value, str):
                    raise ValueError(f"Field '{field}' must be a string")
                elif expected_type.lower() == "int" and not isinstance(value, int):
                    raise ValueError(f"Field '{field}' must be an integer")
                elif expected_type.lower() == "float" and not isinstance(value, (int, float)):
                    raise ValueError(f"Field '{field}' must be a float")
                elif expected_type.lower() == "boolean" and not isinstance(value, bool):
                    raise ValueError(f"Field '{field}' must be a boolean")
                elif expected_type.lower() == "datetime":
                    if isinstance(value, str):
                        # Validate ISO format
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                    else:
                        raise ValueError(f"Field '{field}' must be an ISO 8601 datetime string")
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
                
        # Optional: strictly reject unknown fields
        for field in payload:
            if field not in schema:
                raise HTTPException(status_code=400, detail=f"Strict Schema Violation: Field '{field}' is completely unknown in registry configuration.")

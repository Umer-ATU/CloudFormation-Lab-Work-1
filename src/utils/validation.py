"""
Validation utilities encapsulating request parsing and schema enforcement for
the Items API. Implemented manually to avoid additional dependencies while
still conveying robust guardrails.
"""
import base64
import json
from typing import Any, Dict, Tuple


class ValidationError(Exception):
    """Raised when incoming requests violate business or schema rules."""


def parse_json_body(event: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """
    Attempt to parse the Lambda proxy event body, gracefully handling base64
    encoded payloads as per API Gateway specifications.
    """
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        try:
            body = base64.b64decode(body).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:  # pragma: no cover
            raise ValidationError("Failed to decode base64 body.") from exc
    try:
        parsed = json.loads(body) if body else {}
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON payload: {exc.msg}") from exc
    return parsed, bool(body)


def validate_create_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enforce creation rules:
      * name is mandatory, non-empty string
      * id is optional but, if provided, must be alphanumeric with dashes/underscores
      * description is optional string with sensible length limit
    """
    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Field 'name' is required and must be a non-empty string.")

    validated: Dict[str, Any] = {"name": name.strip()}

    item_id = payload.get("id")
    if item_id is not None:
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValidationError("Field 'id' must be a non-empty string when supplied.")
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
        if not set(item_id).issubset(allowed):
            raise ValidationError("Field 'id' may only contain alphanumeric characters, dash, or underscore.")
        validated["id"] = item_id.strip()

    description = payload.get("description")
    if description is not None:
        if not isinstance(description, str):
            raise ValidationError("Field 'description' must be a string when provided.")
        if len(description) > 1024:
            raise ValidationError("Field 'description' must be less than 1025 characters.")
        validated["description"] = description.strip()

    return validated


def require_path_param(event: Dict[str, Any], name: str) -> str:
    """
    Extract mandatory path parameters from API Gateway proxy events, enforcing
    non-empty values.
    """
    path_params = event.get("pathParameters") or {}
    value = path_params.get(name)
    if not value:
        raise ValidationError(f"Missing required path parameter '{name}'.")
    return value

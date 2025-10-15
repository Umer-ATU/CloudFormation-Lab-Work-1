"""
Response helpers ensuring all Lambda proxy integrations emit consistent JSON
payloads, HTTP status codes, and CORS headers.
"""
import json
from typing import Any, Dict, Optional

# Static CORS configuration aligns with API Gateway method response headers.
_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
}


def success_response(status_code: int, body: Dict[str, Any], extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Build a successful Lambda proxy response with JSON serialized body.
    """
    headers = {**_CORS_HEADERS, **(extra_headers or {})}
    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body),
    }


def error_response(status_code: int, message: str, detail: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Build an error response while preserving consistent envelope for clients.
    """
    payload = {"message": message}
    if detail:
        payload["detail"] = detail
    return success_response(status_code=status_code, body=payload)

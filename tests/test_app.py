from http import HTTPStatus
from types import SimpleNamespace

from src import app


def test_get_tasks_route_returns_placeholder_response():
    event = {"httpMethod": "GET", "resource": "/tasks"}
    context = SimpleNamespace(
        function_name="test-function",
        memory_limit_in_mb=256,
        invoked_function_arn="arn:aws:lambda:local:123456789012:function:test-function",
        aws_request_id="test-request",
    )

    response = app.handler(event, context)

    assert response["statusCode"] == HTTPStatus.OK

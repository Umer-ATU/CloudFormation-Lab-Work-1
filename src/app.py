from __future__ import annotations

import json
import os
from http import HTTPStatus

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
metrics = Metrics(namespace=os.getenv("POWERTOOLS_METRICS_NAMESPACE", "TaskService"))
tracer = Tracer()

TABLE_NAME = os.getenv("TASKS_TABLE_NAME", "")


def _response(status: HTTPStatus, body: dict | list | str) -> dict:
    if not isinstance(body, (dict, list)):
        body = {"message": str(body)}
    return {
        "statusCode": status.value,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


@logger.inject_lambda_context
@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
def handler(event, context):
    """Entry point for API Gateway Lambda proxy integration."""
    logger.info("Received event", extra={"event": event})

    http_method = event.get("httpMethod")
    resource = event.get("resource")

    if resource == "/tasks" and http_method == "GET":
        metrics.add_metric(name="GetTasksInvocations", unit=MetricUnit.Count, value=1)
        # Placeholder implementation until DynamoDB integration is added.
        return _response(
            HTTPStatus.OK,
            {
                "tasks": [],
                "message": "Task list retrieval placeholder",
                "table": TABLE_NAME,
            },
        )

    logger.warning(
        "Unhandled route",
        extra={"http_method": http_method, "resource": resource},
    )
    return _response(HTTPStatus.NOT_IMPLEMENTED, "Route not implemented yet.")

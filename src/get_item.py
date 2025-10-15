"""
Lambda handler implementing GET /items/{id} endpoint.

Retrieves items from DynamoDB and returns structured responses with helpful
error messaging when records do not exist.
"""
import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

from utils.logger import logger, metrics, tracer
from utils.response import error_response, success_response
from utils.validation import ValidationError, require_path_param

_dynamodb = boto3.resource("dynamodb")
_table = _dynamodb.Table(os.environ["TABLE_NAME"])


@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Entry point for Lambda proxy integration.
    """
    try:
        item_id = require_path_param(event, "id")
    except ValidationError as exc:
        logger.warning("Path parameter validation failed", extra={"error": str(exc)})
        metrics.add_metric(name="BadRequest", unit=MetricUnit.Count, value=1)
        return error_response(status_code=400, message=str(exc))

    try:
        response = _table.get_item(Key={"id": item_id})
    except ClientError as exc:
        logger.exception("Failed to retrieve item from DynamoDB")
        metrics.add_metric(name="DynamoDBError", unit=MetricUnit.Count, value=1)
        return error_response(
            status_code=500,
            message="Internal server error while retrieving item.",
            detail={"aws_error": exc.response["Error"]["Message"]},
        )

    item = response.get("Item")
    if not item:
        logger.info("Item not found", extra={"item_id": item_id})
        metrics.add_metric(name="ItemNotFound", unit=MetricUnit.Count, value=1)
        return error_response(status_code=404, message="Item not found.")

    logger.info("Item retrieved successfully", extra={"item_id": item_id})
    metrics.add_metric(name="ItemRetrieved", unit=MetricUnit.Count, value=1)
    return success_response(
        status_code=200,
        body={
            "message": "Item retrieved successfully.",
            "item": item,
        },
    )

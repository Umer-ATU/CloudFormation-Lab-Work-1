"""
Lambda handler implementing POST /items endpoint.

Responsibilities:
  * Parse and validate incoming JSON payloads
  * Persist items into DynamoDB with a generated identifier when necessary
  * Emit structured logs, metrics, and traces via AWS Lambda Powertools
"""
import os
import time
import uuid
from typing import Any, Dict

import boto3
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

from utils.logger import logger, metrics, tracer
from utils.response import error_response, success_response
from utils.validation import ValidationError, parse_json_body, validate_create_payload

# Initialise DynamoDB client lazily but outside the handler to leverage runtime reuse.
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
        payload, has_body = parse_json_body(event)
        if not has_body:
            raise ValidationError("Request body is required for this endpoint.")
        validated_payload = validate_create_payload(payload)
    except ValidationError as exc:
        logger.warning("Validation failed", extra={"error": str(exc)})
        metrics.add_metric(name="BadRequest", unit=MetricUnit.Count, value=1)
        return error_response(status_code=400, message=str(exc))

    # Generate a collision-resistant identifier when client does not supply one.
    item_id = validated_payload.get("id") or uuid.uuid4().hex

    item = {
        "id": item_id,
        "name": validated_payload["name"],
        "createdAt": int(time.time()),
    }
    if "description" in validated_payload:
        item["description"] = validated_payload["description"]

    try:
        # Conditional write prevents accidental overwrites when client provides ids.
        put_args: Dict[str, Any] = {"Item": item}
        if "id" in validated_payload:
            put_args["ConditionExpression"] = "attribute_not_exists(id)"
        _table.put_item(**put_args)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            logger.info("Duplicate id detected", extra={"id": item_id})
            metrics.add_metric(name="Conflict", unit=MetricUnit.Count, value=1)
            return error_response(
                status_code=409,
                message="Item with the provided id already exists.",
            )
        logger.exception("Failed to persist item to DynamoDB")
        metrics.add_metric(name="DynamoDBError", unit=MetricUnit.Count, value=1)
        return error_response(
            status_code=500,
            message="Internal server error while storing item.",
            detail={"aws_error": exc.response["Error"]["Message"]},
        )

    logger.info("Item created successfully", extra={"item_id": item_id})
    metrics.add_metric(name="ItemCreated", unit=MetricUnit.Count, value=1)
    return success_response(
        status_code=201,
        body={
            "message": "Item created successfully.",
            "item": item,
        },
    )

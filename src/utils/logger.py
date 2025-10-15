"""
Utility module centralising AWS Lambda Powertools instrumentation.

Exposes shared Logger, Tracer, and Metrics instances so that business logic
modules can import consistent observability primitives while preserving the
single-source-of-truth configuration (service name, level, etc.).
"""
import os

from aws_lambda_powertools import Logger, Metrics, Tracer


# Derive service metadata from environment variables injected by CloudFormation.
_service_name = os.getenv("POWERTOOLS_SERVICE_NAME", "ItemsApi")
_metrics_namespace = os.getenv("POWERTOOLS_METRICS_NAMESPACE", "ItemsApi")

# Logger automatically captures structured JSON logs with correlation data.
logger = Logger(service=_service_name)

# Tracer enables AWS X-Ray segment emission (if tracing enabled on the function).
tracer = Tracer(service=_service_name)

# Metrics records custom business metrics via CloudWatch Embedded Metric Format.
metrics = Metrics(namespace=_metrics_namespace, service=_service_name)

# CloudFormation Lambda REST API Lab

This repository captures the incremental build-out of a serverless REST API provisioned with AWS CloudFormation. It addresses the lab requirements around Lambda, RESTful services, and infrastructure as code best practices.

## Project Goals
- Deploy an API Gateway REST API backed by AWS Lambda using a CloudFormation template.
- Demonstrate best practices: least-privilege IAM, structured logging, request validation, automated testing, and observability.
- Extend beyond tutorial baselines by integrating DynamoDB storage and AWS Lambda Powertools.
- Produce clear documentation and daily commits showing continuous improvement.

See `docs/architecture-plan.md` for the detailed architecture roadmap.

## Getting Started
1. Ensure Python 3.11+ and AWS CLI v2 are installed.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Package and deploy with the AWS SAM CLI or `aws cloudformation deploy` (commands forthcoming as the project evolves).

## Daily Progress Log
Daily updates, decisions, and enhancements will be documented in `docs/progress-log.md`.

## References
- AWS sample: [API Gateway request validation with CloudFormation](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-validation-sample-cloudformation.html)
- AWS Lambda IaC guidance: [docs.aws.amazon.com/lambda/latest/dg/foundation-iac.html](https://docs.aws.amazon.com/lambda/latest/dg/foundation-iac.html)

# CloudFormation Lambda REST API Project Plan

## Context
- Goal: build an AWS Lambda backed REST API provisioned entirely via CloudFormation, demonstrating practitioner-level understanding of IaC, serverless API design, and deployment pipeline best practice.
- Baseline tutorial: AWS sample `api-gateway-request-validation-sample-cloudformation` for structure; we will extend functionality, tighten security, and add observability.
- Domain: Task tracking service with CRUD endpoints and environment-specific configuration.

## Target Architecture
- **API Gateway (REST):** Public REST API with /tasks resource; request validation, stage variables, logging enabled.
- **Lambda Function (Python 3.11):** Handler implements CRUD operations against DynamoDB; uses AWS Lambda Powertools (logging, tracing, metrics) and follows clean architecture.
- **DynamoDB Table:** Stores task items keyed by `taskId`; on-demand capacity for scalability.
- **IAM Roles & Policies:** Least privilege execution role for Lambda; deployment role for CloudFormation exports.
- **Deployment Pipeline Considerations:** Template linting (`cfn-lint`), unit tests (`pytest`), and automation hooks for GitHub Actions (future step).
- **Observability:** Structured logging, tracing (AWS X-Ray), and custom metrics via Powertools.
- **Security:** IAM authorizer placeholder, API key usage plan for future enhancement, encryption at rest (DynamoDB default), environment variable secrets to be sourced from AWS Parameters (stretch goal).

## Work Breakdown
1. **Scaffold project**
   - Initialise git repo, python virtualenv, and project structure (`src/`, `template/`, `tests/`).
   - Add base CloudFormation template with API Gateway + Lambda skeleton.
2. **Implement Lambda service**
   - Write modular application code with Powertools utilities.
   - Add request/response models, validation, and error handling.
3. **Infrastructure Hardening**
   - Configure IAM roles, logging, throttling, and stage settings.
   - Add DynamoDB table and environment variables.
4. **Testing & Tooling**
   - Add unit tests for handler logic.
   - Configure linting/formatting (e.g., `black`, `flake8`, `cfn-lint`).
5. **Documentation & Write-Up**
   - Maintain README with architecture diagrams and deployment instructions.
   - Draft lab report log capturing daily commits and enhancements.
6. **Stretch Enhancements**
   - Add CI workflow (GitHub Actions) for lint/test.
   - Integrate Parameter Store/Secrets Manager for config.
   - Implement request authorizer or Lambda@Edge caching strategy.

## Next Immediate Actions
1. Initialise git repository and commit baseline docs.
2. Create minimal CloudFormation template and Lambda placeholder.
3. Set up Python environment with Powertools dependency.

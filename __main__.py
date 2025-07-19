"""
Create a Lambda application for creature encounters
"""
import json

import pulumi
import pulumi_aws as aws

lambda_role = aws.iam.Role(
    "randomEncounterLambdaRole",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Effect": "Allow",
            "Sid": ""
        }]
    })
)

aws.iam.RolePolicyAttachment(
    "randomEncounterLambdaBasicExecution",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)



# lambda Function
lambda_function = aws.lambda_.Function(
    "randomEncounterLambdaFunction",
    role=lambda_role.arn,
    runtime=aws.lambda_.Runtime.PYTHON3D12,
    handler="random_encounter.handler",
    timeout=10,
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    })
)

# API Gateway
api = aws.apigatewayv2.Api(
    "encounterApi",
    protocol_type="HTTP",
)

# Integration
integration = aws.apigatewayv2.Integration(
    "randomEncounterIntegration",
    api_id=api.id,
    integration_type="AWS_PROXY",
    integration_uri=lambda_function.invoke_arn,
    integration_method="POST",
    payload_format_version="2.0"
)

# Attach integration to route
get_route = aws.apigatewayv2.Route(
    "randomEncounterGetRoute",
    api_id=api.id,
    route_key="GET /encounter",
    target=integration.id.apply(lambda int_id: f'integrations/{int_id}')
)

# Deploy
stage = aws.apigatewayv2.Stage(
    "defaultStage",
    api_id=api.id,
    name="$default",
    auto_deploy=True,
)

permission = aws.lambda_.Permission(
    "apiGatewayPermission",
    action="lambda:invokeFunction",
    principal="apigateway.amazonaws.com",
    function=lambda_function.name,
    source_arn=api.execution_arn.apply(lambda arn: f"{arn}/*/*"),
)

# ---- Dynamo ----
monsters_table = aws.dynamodb.Table(
    "Monsters",
    name="Monsters",
    attributes=[
        {"name": "id", "type": "S"},
    ],
    hash_key="id",
    billing_mode="PAY_PER_REQUEST",
)

history_table = aws.dynamodb.Table(
    "EncounterHistory",
    name="EncounterHistory",
    attributes=[
        {"name": "timestamp", "type": "S"},
    ],
    hash_key="timestamp",
    billing_mode="PAY_PER_REQUEST",
)

lambda_policy = aws.iam.RolePolicy(
    "lambdaDynamoPolicy",
    role=lambda_role.name,
    policy=aws.iam.get_policy_document_output(
        statements=[{
            "actions": [
                "dynamodb:Scan",
                "dynamodb:PutItem"
            ],
            "resources": [
                monsters_table.arn
            ],
            "effect": "Allow",
        }]
    ).json
)

# Output endpoint URL
pulumi.export(
    "endpoint",
    api.api_endpoint,
)


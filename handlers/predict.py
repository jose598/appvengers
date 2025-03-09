import json
import boto3


def main(event, context):
    sfClient = boto3.client("stepfunctions")
    
    inputData = json.loads(event["body"])
    
    response = sfClient.start_execution(
        stateMachineArn="arn:aws:states:us-west-2:575809686199:stateMachine:analisisCredito",
        input=json.dumps(inputData)
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Análisis iniciado", "executionArn": response["executionArn"]})
    }

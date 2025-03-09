import boto3
import json

def tradicional(event, context):
    sm_runtime = boto3.client("sagemaker-runtime")
    
    payload = json.dumps(event)
    
    response = sm_runtime.invoke_endpoint(
        EndpointName="tradicional",
        ContentType="application/json",
        Body=payload
    )
    
    result = json.loads(response["Body"].read().decode())
    return result
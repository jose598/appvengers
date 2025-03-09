import boto3
import json

def NetworkingAccelerator(event, context):
    sm_runtime = boto3.client("sagemaker-runtime")
    
    payload = json.dumps(event)
    
    response = sm_runtime.invoke_endpoint(
        EndpointName="AppVengersAccelerator",
        ContentType="application/json",
        Body=payload
    )
    
    result = json.loads(response["Body"].read().decode())
    return result

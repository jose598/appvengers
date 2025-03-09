import boto3
import json
import os

sagemaker = boto3.client("sagemaker")

def createEndpointModel(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    model_key = event["Records"][0]["s3"]["object"]["key"]

    model_name = os.path.splitext(os.path.basename(model_key))[0]
    region = "us-west-2"
    container_image = f"683313688378.dkr.ecr.{region}.amazonaws.com/sagemaker-scikit-learn"

    response = sagemaker.create_model(
        ModelName=model_name,
        PrimaryContainer={
            "Image": container_image,
            "ModelDataUrl": f"s3://{bucket_name}/{model_key}"
        },
        ExecutionRoleArn="arn:aws:iam::575809686199:role/SageMakerExecutionRole"
    )

    print(f"Modelo {model_name} creado en SageMaker.")

    response = sagemaker.create_endpoint_config(
        EndpointConfigName=model_name + "-config",
        ProductionVariants=[
            {
                "VariantName": "AllTraffic",
                "ModelName": model_name,
                "InitialInstanceCount": 1,
                "InstanceType": "ml.m5.large",
                "InitialVariantWeight": 1.0,
            }
        ]
    )

    print(f"Configuración del endpoint creada.")

    # Crear el endpoint en SageMaker
    response = sagemaker.create_endpoint(
        EndpointName=model_name,
        EndpointConfigName=model_name + "-config"
    )

    print(f"Endpoint {model_name} desplegado en SageMaker.")

    return {"message": "Endpoint creado correctamente."}

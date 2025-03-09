import boto3
import time

sagemaker = boto3.client("sagemaker")
sns = boto3.client("sns")

def trainingModel(event, context):
    if not event.get("train", False):
        print("No hay nuevos datos, se cancela el entrenamiento.")
        return

    training_job_name = f"model-credit-{int(time.time())}"

    response = sagemaker.create_training_job(
        TrainingJobName=training_job_name,
        AlgorithmSpecification={"TrainingImage": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost"},
        RoleArn="arn:aws:iam::123456789012:role/SageMakerExecutionRole",
        InputDataConfig=[
            {"ChannelName": "train", "DataSource": {"S3DataSource": {"S3Uri": "s3://dev-appvengers-createendpointmodel/credit/newData/"}}}
        ],
        OutputDataConfig={"S3OutputPath": "s3://dev-appvengers-createendpointmodel/credit/"},
        ResourceConfig={"InstanceType": "ml.m5.large", "InstanceCount": 1, "VolumeSizeInGB": 10},
        StoppingCondition={"MaxRuntimeInSeconds": 3600}
    )

    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:123456789012:ReentrenamientoNotificaciones",
        Message=f"Entrenamiento iniciado: {response['TrainingJobArn']}",
        Subject="Nuevo Modelo en Entrenamiento"
    )

    return {"training_job_name": training_job_name}

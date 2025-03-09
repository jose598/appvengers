import boto3

sagemaker = boto3.client("sagemaker")
sns = boto3.client("sns")

def updateModel(event, context):
    training_job_name = event.get("training_job_name")
    if not training_job_name:
        print("No hay modelo nuevo, se cancela la actualización.")
        return

    model_name = f"modelo-creditos-{training_job_name}"

    response = sagemaker.create_model(
        ModelName=model_name,
        PrimaryContainer={
            "Image": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost",
            "ModelDataUrl": f"s3://mi-bucket-modelos/creditos/{training_job_name}/output/model.tar.gz",
        },
        ExecutionRoleArn="arn:aws:iam::123456789012:role/SageMakerExecutionRole"
    )

    response = sagemaker.update_endpoint(
        EndpointName="modelo-creditos-endpoint",
        EndpointConfigName=model_name
    )

    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:123456789012:ReentrenamientoNotificaciones",
        Message="El modelo en producción ha sido actualizado.",
        Subject="Modelo Actualizado"
    )

    print("Modelo actualizado en producción.")

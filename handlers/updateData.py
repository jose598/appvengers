import boto3


def updateData(event, context):
    s3 = boto3.client("s3")
    sns = boto3.client("sns")
    bucket_name = "dev-appvengers-createendpointmodel"
    prefix = "credit/newData/"

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    if "Contents" in response:
        print("Nuevos datos encontrados.")
        boto3.client("lambda").invoke(FunctionName="trainingModel")
        sns.publish(
            TopicArn="arn:aws:sns:us-east-1:123456789012:ReentrenamientoNotificaciones",
            Message="Se han detectado nuevos datos. El modelo se reentrenará.",
            Subject="Reentrenamiento Automático Iniciado"
        )
        return {"train": True}
    else:
        print("No hay datos nuevos.")
        return {"train": False}

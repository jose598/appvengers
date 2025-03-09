import boto3
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("dev-appvengers-PrediccionesCredito")

def saveResult(event, context):
    predictions = event["predictions"]
    
    item = {
        "clientId": event["clientId"],
        "predictions": predictions
    }
    
    table.put_item(Item=item)
    
    return "Exito"

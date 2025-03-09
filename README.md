# **AppVengers - Arquitectura Serverless para Análisis y Reentrenamiento de Modelos de Crédito**

## **📌 Descripción del Proyecto**
Este proyecto implementa una arquitectura **serverless** utilizando **AWS Lambda, Step Functions, DynamoDB, SageMaker y S3** para el análisis de crédito y el reentrenamiento de modelos del **Banco Guayaquil / Grupo AppVengers**.

✅ **Análisis de crédito basado en múltiples modelos**.  
✅ **Automatización del reentrenamiento de modelos en SageMaker**.  
✅ **Almacenamiento de predicciones en DynamoDB**.  
✅ **Manejo de eventos con Step Functions**.  
✅ **Notificaciones con SNS**.  

---

## **📌 Tecnologías Usadas**
- **AWS Lambda** (Ejecuta lógica de predicción y reentrenamiento)
- **AWS Step Functions** (Orquestación de análisis y reentrenamiento)
- **Amazon S3** (Almacén de modelos para inferencia)
- **Amazon SageMaker** (Entrenamiento y actualización de modelos)
- **Amazon DynamoDB** (Almacén de predicciones)
- **Amazon SNS** (Notificaciones de reentrenamiento)
- **Serverless Framework** (Gestión de infraestructura como código)

---

## **📌 Instalación y Configuración**

### **1️⃣ Requisitos Previos**
- AWS CLI configurado (`aws configure`).
- Serverless Framework instalado:
  ```bash
  npm install -g serverless
  ```
- Permisos de **IAM** configurados.

### **2️⃣ Clonar el Proyecto**
```bash
git clone https://github.com/tu-repositorio.git
cd tu-repositorio
```

### **3️⃣ Desplegar con Serverless Framework**
```bash
serverless deploy
```

---

## **📌 Configuración en `serverless.yml`**

```yaml
service: appvengers

provider:
  name: aws
  runtime: python3.10
  memorySize: 512  
  timeout: 30
  tracing: true
  profile: appvengers
  stage: ${opt:stage, 'dev'}
  region: us-west-2
  architecture: arm64
  apiGateway:
    apiKeys:
      - appVengersAPI
  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:*
        - s3:*
        - lambda:*
        - sagemaker:*
        - sns:*
        - states:*
      Resource: "*"
```

---

## **📌 Funciones Lambda Implementadas**

### **📌 Predicción de Crédito**
```yaml
predict:
  handler: handlers/predict.main
  events:
    - http:
        path: predict
        method: post
        private: true
        cors: true
```

### **📌 Reentrenamiento Automático**
```yaml
updateData:
  handler: handlers/updateData.updateData
  events:
    - schedule: rate(7 days)
```

### **📌 Creación Automática de Endpoints en SageMaker**
```yaml
createEndpointModel:
  handler: handlers/createEndpointModel.createEndpointModel
  events:
    - s3:
        bucket:
          Ref: createEndpointModelBucket
        event: s3:ObjectCreated:Put
        rules:
          - prefix: appvengers/
        existing: true
```

---

## **📌 Step Functions: Orquestación del Análisis de Crédito**

```yaml
stepFunctions:
  stateMachines:
    analisisCredito:
      name: "analisisCredito"
      definition:
        StartAt: "Start Model"
        States:
          Start Model:
            Type: "Parallel"
            Branches:
              - StartAt: "Tradicional"
                States:
                  Tradicional:
                    Type: "Task"
                    Resource: "arn:aws:lambda:us-west-2:575809686199:function:appvengers-dev-Tradicional"
                    End: true
              - StartAt: "NetworkingAccelerator"
                States:
                  NetworkingAccelerator:
                    Type: "Task"
                    Resource: "arn:aws:lambda:us-west-2:575809686199:function:appvengers-dev-NetworkingAccelerator"
                    End: true
              - StartAt: "AppVengersAccelerator"
                States:
                  AppVengersAccelerator:
                    Type: "Task"
                    Resource: "arn:aws:lambda:us-west-2:575809686199:function:appvengers-dev-AppVengersAccelerator"
                    End: true
            Next: "SaveResult"

          SaveResult:
            Type: "Task"
            Resource: "arn:aws:lambda:us-west-2:575809686199:function:appvengers-dev-saveResult"
            End: true
```

---

## **📌 Recursos Adicionales**

### **📌 DynamoDB: Almacenamiento de Predicciones**
```yaml
PrediccionesCredito:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: ${self:provider.stage}-${self:service}-PrediccionesCredito
    AttributeDefinitions:
      - AttributeName: clientId
        AttributeType: S
    KeySchema:
      - AttributeName: clientId
        KeyType: HASH
    BillingMode: PAY_PER_REQUEST
```

### **📌 SNS para Notificaciones de Reentrenamiento**
```yaml
ReentrenamientoNotificaciones:
  Type: AWS::SNS::Topic
  Properties:
    TopicName: ${self:provider.stage}-${self:service}-ReentrenamientoNotificaciones
```

### **📌 S3 para Modelos**
```yaml
createEndpointModelBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: ${self:provider.stage}-${self:service}-createendpointmodel
    CorsConfiguration:
      CorsRules:
        - AllowedOrigins:
            - '*'
          AllowedHeaders:
            - '*'
          AllowedMethods:
            - GET
            - PUT
            - POST
            - DELETE
            - HEAD
```

---

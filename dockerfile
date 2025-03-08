FROM public.ecr.aws/lambda/python:3.10
RUN pip install --no-cache-dir joblib scikit-learn pandas numpy
COPY lambda_function.py .
CMD ["lambda_function.lambda_handler"]

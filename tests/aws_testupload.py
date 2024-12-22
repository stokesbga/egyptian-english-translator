import boto3
import json


post_data = {
    "files": [("audio_file", open("app/demo.wav", "rb"))]
}

# Endpoint name
endpoint_name = 'eg-en-translator-endpoint'

# Invoke SageMaker endpoint
client = boto3.client('sagemaker-runtime', region_name='us-east-1')
response = client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=json.dumps(post_data)
)

# Deserialize the response
response_body = response['Body'].read().decode('utf-8')
response_json = json.loads(response_body)

# Get predictions
print(response_json)
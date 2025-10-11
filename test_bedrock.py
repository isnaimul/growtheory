import boto3
import json

# we initialize the bedrock client to perform actions:
# link to boto api documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
# link to bedrock-runtime api documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# simple prompt string
prompt = "Say hello and explain what you are."

# we call nova micro via the invoke_model function for the bedrock-runtime
# body is expected to be a json-formatted string, so we write data as python dict and convert it to a json string
response = bedrock.invoke_model(
    modelId="amazon.nova-micro-v1:0",
    body=json.dumps(
        {
            "messages": [{"role": "user", "content": "hello"}],
            "max_tokens": 100,
            "temperature": 0.7,
        }
    ),
)

# we get a dict back
result = json.loads(response["body".read()])
print(result["output"]["message"]["content"][0]["text"])

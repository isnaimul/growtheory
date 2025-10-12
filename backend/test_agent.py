import boto3
import json

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

AGENT_ID='ME47KYRCL8'
AGENT_ALIAS_ID='S2KLOUJIPS'

def test_agent(prompt):
    """Test the agent with a prompt"""
    
    print(f"\nPrompt: {prompt}\n")
    
    response = client.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId='test-session-123',
        inputText=prompt
    )
    
    # Parse streaming response
    result = ""
    for event in response['completion']:
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                result += chunk['bytes'].decode('utf-8')
    
    print("Response:")
    print(result)
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_agent("Tell me about Amazon")
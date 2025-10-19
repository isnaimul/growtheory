import boto3
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

dynamodb = boto3.resource('dynamodb')
cache_table = dynamodb.Table('GrowTheory-CompanyCache')

print("=" * 50)
print("Testing DynamoDB Connection")
print("=" * 50)

# Test 1: Write
print("\n1. Testing WRITE to DynamoDB...")
try:
    cache_table.put_item(Item={
        'ticker': 'TEST',
        'company': 'Test Company',
        'timestamp': '2024-10-18T12:00:00',
        'expiresAt': 1729800000,
        'score': 85,
        'grade': 'A',
        'full_analysis': 'This is a test analysis'
    })
    print("   ✓ Write successful")
except Exception as e:
    print(f"   ✗ Write failed: {e}")
    sys.exit(1)

# Test 2: Read
print("\n2. Testing READ from DynamoDB...")
try:
    response = cache_table.get_item(Key={'ticker': 'TEST'})
    if 'Item' in response:
        print(f"   ✓ Read successful")
        print(f"   Found: {response['Item']['company']} (Grade: {response['Item']['grade']})")
    else:
        print("   ✗ Read failed: Item not found")
except Exception as e:
    print(f"   ✗ Read failed: {e}")

# Test 3: Scan (dashboard functionality)
print("\n3. Testing SCAN (dashboard query)...")
try:
    response = cache_table.scan()
    count = len(response.get('Items', []))
    print(f"   ✓ Scan successful")
    print(f"   Found {count} total items in cache")
    
    for item in response.get('Items', [])[:3]:
        print(f"   - {item['company']} ({item['ticker']}): {item['grade']}")
    
except Exception as e:
    print(f"   ✗ Scan failed: {e}")

# Test 4: Delete test item
print("\n4. Cleaning up test data...")
try:
    cache_table.delete_item(Key={'ticker': 'TEST'})
    print("   ✓ Cleanup successful")
except Exception as e:
    print(f"   ✗ Cleanup failed: {e}")

print("\n" + "=" * 50)
print("DynamoDB Connection Test Complete! ✓")
print("=" * 50)
import requests
import os

YOU_API_KEY = os.getenv("YOU_API_KEY", "ydc-sk-fef5ec29a1fdd9b1-pxy1kM4juRSUqSTirF7ng7fh12hxp2G1-e467f801<__>1SNetLETU8N2v5f4Zab03FiX")
YOU_API_URL = "https://api.you.com/v1/agents/runs"

print("Testing You.com API...")
print(f"API Key: {YOU_API_KEY[:20]}...")

try:
    response = requests.post(
        YOU_API_URL,
        headers={
            'Authorization': f'Bearer {YOU_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'agent': 'advanced',
            'input': 'Write a short marketing tagline for Tesla',
            'stream': False
        },
        timeout=30
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ API WORKS!")
        print(f"Output: {data.get('output', [{}])[0].get('content', 'No content')[:200]}")
    else:
        print(f"\n❌ API ERROR: {response.status_code}")
        print(f"Message: {response.text}")
        
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")
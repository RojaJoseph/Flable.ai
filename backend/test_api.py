"""
Quick API Test Script
Tests login, dashboard, and campaigns endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("="*60)
    print("Testing Flable.ai API")
    print("="*60)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing Login...")
    login_data = {
        "email": "demo@flable.ai",
        "password": "demo123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            print(f"   ✅ Login successful!")
            print(f"   Access Token: {access_token[:20]}...")
            print(f"   Refresh Token: {refresh_token[:20]}...")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 3: Dashboard (without trailing slash)
    print("\n3. Testing Dashboard (no slash)...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/dashboard", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Dashboard loaded successfully!")
            data = response.json()
            print(f"   Stats: {data.get('stats', {})}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Dashboard (with trailing slash)
    print("\n4. Testing Dashboard (with slash)...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/dashboard/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Dashboard loaded successfully!")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Campaigns
    print("\n5. Testing Campaigns...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/campaigns?limit=10", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            campaigns = response.json()
            print(f"   ✅ Campaigns loaded successfully!")
            print(f"   Total campaigns: {len(campaigns)}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Refresh Token
    print("\n6. Testing Token Refresh...")
    try:
        refresh_data = {"refresh_token": refresh_token}
        response = requests.post(f"{BASE_URL}/api/v1/auth/refresh", json=refresh_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            new_tokens = response.json()
            print(f"   ✅ Token refresh successful!")
            print(f"   New Access Token: {new_tokens['access_token'][:20]}...")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_api()

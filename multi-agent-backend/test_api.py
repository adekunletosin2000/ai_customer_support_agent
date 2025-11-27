"""
Test script for the Flask API
Run this after starting app.py to verify all endpoints work
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def test_health_check():
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_start_chat():
    print_section("Testing Start Chat")
    response = requests.post(
        f"{BASE_URL}/api/chat/start",
        json={"user_id": "test_user_123"}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.status_code == 201:
        return data["session_id"], data["user_id"]
    return None, None

def test_send_message(session_id, user_id, message):
    print_section(f"Testing Send Message: '{message[:50]}...'")
    response = requests.post(
        f"{BASE_URL}/api/chat/message",
        json={
            "session_id": session_id,
            "user_id": user_id,
            "message": message
        }
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Agent Response: {data.get('agent_response', 'No response')[:200]}...")
    print(f"Metadata: {json.dumps(data.get('metadata', {}), indent=2)}")
    return response.status_code == 200

def test_get_history(session_id):
    print_section("Testing Get Chat History")
    response = requests.get(f"{BASE_URL}/api/chat/history/{session_id}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Message Count: {data.get('message_count', 0)}")
    print(f"History Length: {len(data.get('conversation_history', []))}")
    return response.status_code == 200

def test_active_sessions():
    print_section("Testing Get Active Sessions")
    response = requests.get(f"{BASE_URL}/api/sessions/active")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Active Sessions: {data.get('active_sessions', 0)}")
    return response.status_code == 200

def test_end_chat(session_id):
    print_section("Testing End Chat")
    response = requests.post(f"{BASE_URL}/api/chat/end/{session_id}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    return response.status_code == 200

def run_full_test():
    """Run complete test suite"""
    print("\n" + "🚀" * 30)
    print("STARTING COMPREHENSIVE API TEST")
    print("🚀" * 30)
    
    results = {}
    
    # Test 1: Health Check
    results["health_check"] = test_health_check()
    time.sleep(1)
    
    # Test 2: Start Chat
    session_id, user_id = test_start_chat()
    results["start_chat"] = (session_id is not None)
    time.sleep(1)
    
    if not session_id:
        print("\n❌ Failed to create session. Stopping tests.")
        return
    
    # Test 3: Send Messages
    test_messages = [
        "My internet is not working at all! This is very urgent!",
        "I was charged twice on my last bill",
        "How do I update my app?"
    ]
    
    results["send_messages"] = []
    for msg in test_messages:
        success = test_send_message(session_id, user_id, msg)
        results["send_messages"].append(success)
        time.sleep(2)  # Wait for agent processing
    
    # Test 4: Get History
    results["get_history"] = test_get_history(session_id)
    time.sleep(1)
    
    # Test 5: Active Sessions
    results["active_sessions"] = test_active_sessions()
    time.sleep(1)
    
    # Test 6: End Chat
    results["end_chat"] = test_end_chat(session_id)
    time.sleep(1)
    
    # Print Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"✅ Health Check: {'PASSED' if results['health_check'] else 'FAILED'}")
    print(f"✅ Start Chat: {'PASSED' if results['start_chat'] else 'FAILED'}")
    print(f"✅ Send Messages: {sum(results['send_messages'])}/{len(results['send_messages'])} PASSED")
    print(f"✅ Get History: {'PASSED' if results['get_history'] else 'FAILED'}")
    print(f"✅ Active Sessions: {'PASSED' if results['active_sessions'] else 'FAILED'}")
    print(f"✅ End Chat: {'PASSED' if results['end_chat'] else 'FAILED'}")
    
    total_tests = 6 + len(results['send_messages']) - 1
    passed_tests = sum([
        results['health_check'],
        results['start_chat'],
        sum(results['send_messages']),
        results['get_history'],
        results['active_sessions'],
        results['end_chat']
    ])
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        run_full_test()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask server")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
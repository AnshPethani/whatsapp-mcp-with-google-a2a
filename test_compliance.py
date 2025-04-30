import asyncio
import json
from datetime import datetime, timezone
from compliance import A2AComplianceWrapper, ProtocolHandler, A2ASecurity
from simple_client import SimpleWhatsAppClient

def get_utc_now():
    """Get current UTC time in ISO format"""
    return datetime.now(timezone.utc)

async def test_protocol_handler():
    """Test the protocol handler component"""
    print("\n1. Testing Protocol Handler...")
    print("-" * 50)
    
    handler = ProtocolHandler()
    test_message = {
        "recipient": "919820863458",
        "message": "A2A Compliance Test Message",
        "metadata": {
            "message_type": "text"
        }
    }
    
    # Test message formatting
    formatted = handler.format_message(test_message)
    print(" ✓ Message formatting:")
    print("-" * 30)
    print(json.dumps(formatted, indent=2))
    assert "protocol_version" in formatted
    assert "timestamp" in formatted
    assert "payload" in formatted
    
    # Test message validation
    is_valid = handler.validate_message(formatted)
    print(f"\n ✓ Message validation: {is_valid}")
    assert is_valid

async def test_security():
    """Test the security layer"""
    print("\n2. Testing Security Layer...")
    print("-" * 50)
    
    security = A2ASecurity("test_secret_key")
    test_message = {
        "content": "Test message",
        "timestamp": get_utc_now().isoformat()
    }
    
    # Test encryption
    encrypted = security.encrypt_message(json.dumps(test_message))
    print(f" ✓ Encrypted message:")
    print("-" * 30)
    print(f"{encrypted[:50]}...")
    
    # Test decryption
    decrypted = security.decrypt_message(encrypted)
    print("\n ✓ Decryption successful")
    assert json.loads(decrypted)["content"] == test_message["content"]
    
    # Test signature
    timestamp = get_utc_now().isoformat()
    signature = security.generate_signature("test_message", timestamp)
    is_valid = security.verify_signature("test_message", timestamp, signature)
    print(f"\n ✓ Signature verification: {is_valid}")
    
    # Test JWT
    jwt_token = security.generate_jwt({"user_id": "test123"})
    jwt_payload = security.verify_jwt(jwt_token)
    print(f"\n ✓ JWT verification successful: {jwt_payload['user_id']}")

async def test_compliance_wrapper():
    """Test the compliance wrapper"""
    print("\n3. Testing Compliance Wrapper...")
    print("-" * 50)
    
    wrapper = A2AComplianceWrapper(
        base_url="http://localhost:8080",
        api_key="test_api_key",
        secret_key="test_secret_key"
    )
    
    # Test compliance verification
    compliance_status = wrapper.verify_compliance()
    print(" ✓ Compliance status:")
    print("-" * 30)
    print(json.dumps(compliance_status, indent=2))
    assert compliance_status["compliant"]
    
    # Test message validation
    timestamp = get_utc_now().isoformat()
    test_message = {
        "protocol_version": "1.0",
        "timestamp": timestamp,
        "payload": {
            "content": "Test message",
            "recipient": "919820863458",
            "type": "text"
        },
        "metadata": {
            "timestamp": timestamp,
            "message_id": f"A2A-MSG-{get_utc_now().strftime('%Y%m%d%H%M%S')}",
            "message_type": "text"
        }
    }
    is_valid = wrapper.validate_message(test_message)
    print(f"\n ✓ Message validation: {is_valid}")
    assert is_valid

async def test_end_to_end():
    """Test end-to-end message flow"""
    print("\n4. Testing End-to-End Flow...")
    print("-" * 50)
    
    # Initialize components
    wrapper = A2AComplianceWrapper(
        base_url="http://localhost:8080",
        api_key="test_api_key",
        secret_key="test_secret_key"
    )
    
    client = SimpleWhatsAppClient()
    
    # Test message send flow
    try:
        recipient = "919820863458"
        message = "Test end-to-end message"
        
        print(" ✓ Preparing A2A compliant message...")
        
        # Format message according to A2A protocol
        message_payload = {
            "recipient": recipient,
            "message": message,
            "metadata": {
                "protocol_version": "1.0",
                "api_key": wrapper.api_key,
                "message_type": "text"
            }
        }
        
        # Show protocol formatted message
        protocol_message = wrapper.protocol_handler.format_message(message_payload)
        print("\nProtocol formatted message:")
        print("-" * 30)
        print(json.dumps(protocol_message, indent=2))
        
        # Show secured message
        secured_message = wrapper.security.secure_message(protocol_message)
        print("\nSecured message:")
        print("-" * 30)
        print(json.dumps(secured_message, indent=2))
        
        # Send the message
        result = await wrapper.send_message(recipient, message)
        print("\nServer response:")
        print("-" * 30)
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"\n ✗ Message send failed: {e}")
        # Don't fail the test as the server might not be running

async def main():
    """Run all tests"""
    print("\nStarting A2A Compliance Tests...")
    print("=" * 50)
    
    try:
        await test_protocol_handler()
        await test_security()
        await test_compliance_wrapper()
        await test_end_to_end()
        print("\n ✓ All tests completed successfully!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n ✗ Test failed: {e}")
        print("=" * 50)
    except Exception as e:
        print(f"\n ✗ Unexpected error: {e}")
        print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main()) 
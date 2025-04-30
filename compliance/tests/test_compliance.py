import unittest
from datetime import datetime
import json
from ..a2a_wrapper import A2AComplianceWrapper
from ..protocol_handlers import ProtocolHandler, A2AStatus, A2AErrorCode
from ..security import A2ASecurity

class TestA2ACompliance(unittest.TestCase):
    """Test suite for A2A compliance"""
    
    def setUp(self):
        """Set up test environment"""
        self.api_key = "test_api_key"
        self.secret_key = "test_secret_key"
        self.encryption_key = Fernet.generate_key().decode()
        self.wrapper = A2AComplianceWrapper(
            "http://localhost:8080",
            self.api_key,
            self.secret_key
        )
        self.security = A2ASecurity(self.secret_key, self.encryption_key)
        
    def test_message_formatting(self):
        """Test message formatting compliance"""
        payload = {
            "recipient": "1234567890",
            "message": "Test message"
        }
        
        formatted_message = self.wrapper._format_a2a_message(
            "send_message",
            payload
        )
        
        # Check required fields
        required_fields = ["version", "timestamp", "action", "payload", "signature"]
        self.assertTrue(all(field in formatted_message for field in required_fields))
        
        # Check payload structure
        self.assertEqual(formatted_message["payload"], payload)
        
    def test_signature_generation(self):
        """Test signature generation and verification"""
        message = "test message"
        timestamp = datetime.utcnow().isoformat()
        
        signature = self.wrapper._generate_signature(message, timestamp)
        self.assertIsInstance(signature, str)
        self.assertEqual(len(signature), 64)  # SHA-256 hash length
        
    def test_protocol_handlers(self):
        """Test protocol handler compliance"""
        # Test message send handler
        send_payload = {
            "recipient": "1234567890",
            "message": "Test message"
        }
        
        send_response = ProtocolHandler.handle_message_send(send_payload)
        self.assertEqual(send_response["status"], A2AStatus.SUCCESS.value)
        self.assertIn("message_id", send_response["metadata"])
        
        # Test message receive handler
        receive_payload = {
            "sender": "1234567890",
            "message": "Test message",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        receive_response = ProtocolHandler.handle_message_receive(receive_payload)
        self.assertEqual(receive_response["status"], A2AStatus.SUCCESS.value)
        
    def test_security_layer(self):
        """Test security layer compliance"""
        # Test message encryption/decryption
        original_message = {"test": "data"}
        encrypted_message = self.security.encrypt_message(original_message)
        decrypted_message = self.security.decrypt_message(encrypted_message)
        self.assertEqual(original_message, decrypted_message)
        
        # Test JWT generation/verification
        jwt_payload = {"user_id": "123"}
        token = self.security.generate_jwt(jwt_payload)
        verified_payload = self.security.verify_jwt(token)
        self.assertEqual(jwt_payload["user_id"], verified_payload["user_id"])
        
    def test_end_to_end_compliance(self):
        """Test end-to-end A2A compliance"""
        # Create and secure a message
        original_message = {
            "recipient": "1234567890",
            "message": "Test message"
        }
        
        # Format according to A2A protocol
        a2a_message = self.wrapper._format_a2a_message(
            "send_message",
            original_message
        )
        
        # Apply security measures
        secure_message = self.security.secure_message(a2a_message)
        
        # Verify and decrypt
        verified_message = self.security.verify_secure_message(secure_message)
        
        # Check protocol compliance
        self.assertTrue(ProtocolHandler.validate_message_structure(verified_message))
        
        # Verify the message content
        self.assertEqual(verified_message["payload"], original_message)

if __name__ == '__main__':
    unittest.main() 
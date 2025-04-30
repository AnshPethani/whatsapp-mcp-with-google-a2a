from typing import Dict, Any
import base64
import hmac
import hashlib
import json
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import jwt

class A2ASecurity:
    """Security layer for Google A2A protocol compliance"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
    def secure_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply security measures to a message following A2A protocol
        
        Args:
            message: Message to secure
            
        Returns:
            Secured message with encryption and signature
        """
        # Convert message to string for encryption
        message_str = json.dumps(message)
        
        # Generate timestamp for signature
        timestamp = datetime.utcnow().isoformat()
        
        # Encrypt message
        encrypted_message = self.encrypt_message(message_str)
        
        # Generate signature
        signature = self.generate_signature(encrypted_message, timestamp)
        
        return {
            "encrypted_payload": encrypted_message,
            "timestamp": timestamp,
            "signature": signature,
            "encryption_type": "fernet",
            "protocol_version": message.get("protocol_version", "1.0")
        }
        
    def encrypt_message(self, message: str) -> str:
        """
        Encrypt a message using Fernet symmetric encryption
        
        Args:
            message: Message to encrypt
            
        Returns:
            Encrypted message as base64 string
        """
        encrypted = self.cipher_suite.encrypt(message.encode())
        return base64.b64encode(encrypted).decode()
        
    def decrypt_message(self, encrypted_message: str) -> str:
        """
        Decrypt a Fernet-encrypted message
        
        Args:
            encrypted_message: Base64 encoded encrypted message
            
        Returns:
            Decrypted message string
        """
        encrypted_bytes = base64.b64decode(encrypted_message.encode())
        decrypted = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted.decode()
        
    def generate_signature(self, message: str, timestamp: str) -> str:
        """
        Generate HMAC signature for message authentication
        
        Args:
            message: Message to sign
            timestamp: Timestamp to include in signature
            
        Returns:
            Hex-encoded HMAC signature
        """
        message_to_sign = f"{message}{timestamp}"
        signature = hmac.new(
            self.secret_key.encode(),
            message_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
        
    def verify_signature(self, message: str, timestamp: str, signature: str) -> bool:
        """
        Verify message signature
        
        Args:
            message: Original message
            timestamp: Timestamp used in signature
            signature: Signature to verify
            
        Returns:
            bool indicating if signature is valid
        """
        expected_signature = self.generate_signature(message, timestamp)
        return hmac.compare_digest(signature, expected_signature)
        
    def verify_setup(self) -> bool:
        """
        Verify security setup is complete and valid
        
        Returns:
            bool indicating if security setup is valid
        """
        return bool(self.secret_key and self.encryption_key)
        
    def generate_jwt(self, payload: Dict[str, Any], 
                    expiration_minutes: int = 60) -> str:
        """Generate JWT token for authentication."""
        payload['exp'] = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
        
    def verify_jwt(self, token: str) -> Dict[str, Any]:
        """Verify JWT token."""
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
            
    def generate_message_signature(self, message: str, 
                                 timestamp: str) -> str:
        """Generate HMAC signature for message authentication."""
        message_to_sign = f"{message}{timestamp}"
        return hmac.new(
            self.secret_key.encode(),
            message_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()
        
    def verify_message_signature(self, message: str, 
                               timestamp: str, 
                               signature: str) -> bool:
        """Verify message signature."""
        expected_signature = self.generate_message_signature(message, timestamp)
        return hmac.compare_digest(signature, expected_signature)
        
    def verify_secure_message(self, secure_message: Dict[str, Any]) -> Dict[str, Any]:
        """Verify and decrypt a secure message."""
        required_fields = ["encrypted_payload", "timestamp", "signature"]
        if not all(field in secure_message for field in required_fields):
            raise ValueError("Missing required security fields")
            
        # Verify signature
        if not self.verify_signature(
            secure_message["encrypted_payload"],
            secure_message["timestamp"],
            secure_message["signature"]
        ):
            raise ValueError("Invalid message signature")
            
        # Decrypt payload
        return self.decrypt_message(secure_message["encrypted_payload"]) 
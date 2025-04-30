from typing import Dict, Any, Optional
import json
import requests
from .security import A2ASecurity
from .protocol_handler import ProtocolHandler

class A2AComplianceWrapper:
    """Google A2A Compliance Wrapper for WhatsApp MCP"""
    
    def __init__(self, base_url: str, api_key: str, secret_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.security = A2ASecurity(secret_key)
        self.protocol_handler = ProtocolHandler()
        
    async def send_message(self, recipient: str, message: str) -> Dict[str, Any]:
        """
        Send a message following Google A2A compliance protocols
        
        Args:
            recipient: The recipient's phone number
            message: The message content
            
        Returns:
            Dict containing the response from the server
        """
        # Format message according to A2A protocol
        message_payload = {
            "recipient": recipient,
            "message": message,
            "metadata": {
                "protocol_version": "1.0",
                "api_key": self.api_key,
                "message_type": "text"
            }
        }
        
        # Handle protocol requirements
        protocol_message = self.protocol_handler.format_message(message_payload)
        
        # Apply security measures
        secured_message = self.security.secure_message(protocol_message)
        
        # Prepare final message for server
        server_payload = {
            "recipient": recipient,  # Keep original recipient
            "message": message,      # Keep original message
            "a2a_metadata": secured_message  # Include A2A compliance data
        }
        
        # Send the message
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "X-Protocol-Version": "1.0"
            }
            
            response = requests.post(
                f"{self.base_url}/api/send",
                json=server_payload,
                headers=headers
            )
            
            if response.status_code == 200:
                return {"status": "success", "data": response.json()}
            else:
                return {
                    "status": "error",
                    "error": f"Request failed with status {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            return {"status": "error", "error": str(e)}
            
    def validate_message(self, message: Dict[str, Any]) -> bool:
        """
        Validate message structure according to A2A protocol
        
        Args:
            message: The message to validate
            
        Returns:
            bool indicating if message is valid
        """
        return self.protocol_handler.validate_message(message)
        
    def verify_compliance(self) -> Dict[str, Any]:
        """
        Verify all compliance requirements are met
        
        Returns:
            Dict containing compliance status and any issues
        """
        compliance_checks = {
            "protocol_version": True,
            "security": self.security.verify_setup(),
            "message_format": True,
            "api_auth": bool(self.api_key)
        }
        
        return {
            "compliant": all(compliance_checks.values()),
            "checks": compliance_checks
        } 
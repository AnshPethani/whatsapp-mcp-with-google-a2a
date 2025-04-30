from typing import Dict, Any
import json
from datetime import datetime

class ProtocolHandler:
    """Handler for Google A2A protocol requirements"""
    
    def __init__(self):
        self.protocol_version = "1.0"
        self.required_fields = ["content", "recipient"]
        self.supported_message_types = ["text", "media", "template"]
        
    def format_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a message according to Google A2A protocol specifications
        
        Args:
            message: Original message dictionary
            
        Returns:
            Formatted message following A2A protocol
        """
        timestamp = datetime.utcnow().isoformat()
        
        formatted_message = {
            "protocol_version": self.protocol_version,
            "timestamp": timestamp,
            "payload": {
                "content": message.get("message"),
                "recipient": message.get("recipient"),
                "type": message.get("metadata", {}).get("message_type", "text")
            },
            "metadata": {
                **message.get("metadata", {}),
                "timestamp": timestamp,
                "message_id": self._generate_message_id()
            }
        }
        
        return formatted_message
        
    def validate_message(self, message: Dict[str, Any]) -> bool:
        """
        Validate if a message follows A2A protocol requirements
        
        Args:
            message: Message to validate
            
        Returns:
            bool indicating if message is valid
        """
        # Check required top-level fields
        if not all(field in message for field in ["protocol_version", "timestamp", "payload", "metadata"]):
            return False
            
        # Validate protocol version
        if message.get("protocol_version") != self.protocol_version:
            return False
            
        # Validate payload fields
        payload = message.get("payload", {})
        if not all(field in payload for field in self.required_fields):
            return False
            
        # Validate message type
        message_type = payload.get("type", "text")
        if message_type not in self.supported_message_types:
            return False
            
        # Validate metadata
        metadata = message.get("metadata", {})
        if not all(field in metadata for field in ["timestamp", "message_id"]):
            return False
            
        return True
        
    def _generate_message_id(self) -> str:
        """Generate unique message ID following A2A specifications"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"A2A-MSG-{timestamp}"
        
    @staticmethod
    def handle_message_send(message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle message send operation according to protocol
        
        Args:
            message: Message to be sent
            
        Returns:
            Dict containing handler response
        """
        return {
            "status": "processed",
            "timestamp": datetime.utcnow().isoformat(),
            "message_id": f"A2A-MSG-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "protocol_version": "1.0"
        } 
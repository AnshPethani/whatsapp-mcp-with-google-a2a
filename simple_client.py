import aiohttp
from typing import Dict, Any, Optional
import json

class SimpleWhatsAppClient:
    """Simple WhatsApp client for MCP system"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        
    async def send_message(self, 
                         recipient: str, 
                         message: str,
                         message_type: str = "text") -> Dict[str, Any]:
        """
        Send a WhatsApp message through the MCP system
        
        Args:
            recipient: Recipient's phone number
            message: Message content
            message_type: Type of message (text, media, template)
            
        Returns:
            Dict containing the response from the server
        """
        # Format phone number if needed
        if not recipient.startswith('91'):
            recipient = '91' + recipient
            
        payload = {
            "recipient": recipient,
            "message": message
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/api/send",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        return {"status": "success", "data": await response.json()}
                    else:
                        return {
                            "status": "error",
                            "error": f"Request failed with status {response.status}",
                            "details": await response.text()
                        }
            except Exception as e:
                return {"status": "error", "error": str(e)}
                
    async def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Get status of a sent message
        
        Args:
            message_id: ID of the message to check
            
        Returns:
            Dict containing message status
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.base_url}/api/status/{message_id}"
                ) as response:
                    if response.status == 200:
                        return {"status": "success", "data": await response.json()}
                    else:
                        return {
                            "status": "error",
                            "error": f"Request failed with status {response.status}"
                        }
            except Exception as e:
                return {"status": "error", "error": str(e)} 
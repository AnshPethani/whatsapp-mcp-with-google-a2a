# WhatsApp MCP Google A2A Compliance Layer

This module provides Google Agent-to-Agent (A2A) protocol compliance for WhatsApp MCP. It enables secure, standardized communication between AI agents through WhatsApp while adhering to Google's A2A specifications.

## Quick Start

```python
from compliance import A2AComplianceWrapper

# Initialize the wrapper
wrapper = A2AComplianceWrapper(
    base_url="http://localhost:8080",
    api_key="your_api_key",
    secret_key="your_secret_key"
)

# Send an A2A compliant message
async def send_message():
    result = await wrapper.send_message(
        recipient="919876543210",
        message="Hello from A2A compliant WhatsApp!"
    )
    print(result)
```

## Components

### 1. Compliance Wrapper (`a2a_wrapper.py`)
Main interface that coordinates A2A compliance:
```python
wrapper = A2AComplianceWrapper(base_url, api_key, secret_key)
result = await wrapper.send_message(recipient, message)
status = wrapper.verify_compliance()
```

### 2. Protocol Handler (`protocol_handler.py`)
Manages message formatting and validation:
```python
handler = ProtocolHandler()
formatted = handler.format_message({
    "recipient": "919876543210",
    "message": "Hello",
    "metadata": {"message_type": "text"}
})
```

### 3. Security Layer (`security.py`)
Handles encryption, signatures, and authentication:
```python
security = A2ASecurity(secret_key)
secured = security.secure_message(message)
token = security.generate_jwt({"user_id": "123"})
```

## Message Structure

A2A compliant messages follow this structure:
```json
{
    "protocol_version": "1.0",
    "timestamp": "2024-04-30T10:00:00Z",
    "payload": {
        "content": "Hello World",
        "recipient": "919876543210",
        "type": "text"
    },
    "metadata": {
        "message_type": "text",
        "timestamp": "2024-04-30T10:00:00Z",
        "message_id": "A2A-MSG-20240430100000"
    }
}
```

## Security Features

1. **Message Encryption**
   - Fernet symmetric encryption
   - Secure key management
   - Encrypted payload transmission

2. **Message Signing**
   - HMAC-SHA256 signatures
   - Timestamp validation
   - Replay attack prevention

3. **Authentication**
   - JWT token support
   - API key validation
   - Signature verification

## Testing

Run the test suite:
```bash
python test_compliance.py
```

The tests verify:
- Protocol compliance
- Message encryption/decryption
- Signature verification
- End-to-end message flow

## Error Handling

```python
try:
    result = await wrapper.send_message(recipient, message)
    if result["status"] == "error":
        print(f"Error: {result['error']}")
except Exception as e:
    print(f"Failed to send message: {e}")
```

## Best Practices

1. **API Key Management**
   ```python
   # Use environment variables
   import os
   api_key = os.getenv("WHATSAPP_API_KEY")
   secret_key = os.getenv("WHATSAPP_SECRET_KEY")
   ```

2. **Message Validation**
   ```python
   # Always validate before sending
   if wrapper.validate_message(message):
       result = await wrapper.send_message(recipient, message)
   ```

3. **Security Setup**
   ```python
   # Verify security configuration
   security_status = wrapper.verify_compliance()
   if not security_status["compliant"]:
       raise SecurityError("Compliance check failed")
   ```

## Common Issues

1. **Connection Errors**
   ```
   Error: Connection refused
   Solution: Verify WhatsApp MCP server is running on correct port
   ```

2. **Authentication Failures**
   ```
   Error: Invalid API key
   Solution: Check API key configuration and validity
   ```

3. **Protocol Errors**
   ```
   Error: Invalid message format
   Solution: Verify message structure matches A2A specification
   ```

## Integration Example

Complete integration with error handling and validation:

```python
from compliance import A2AComplianceWrapper
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppA2AClient:
    def __init__(self):
        self.wrapper = A2AComplianceWrapper(
            base_url=os.getenv("WHATSAPP_MCP_URL", "http://localhost:8080"),
            api_key=os.getenv("WHATSAPP_API_KEY"),
            secret_key=os.getenv("WHATSAPP_SECRET_KEY")
        )
        
        # Verify compliance setup
        status = self.wrapper.verify_compliance()
        if not status["compliant"]:
            raise RuntimeError("A2A compliance check failed")
            
    async def send_message(self, recipient: str, message: str):
        try:
            # Send with full A2A compliance
            result = await self.wrapper.send_message(recipient, message)
            
            if result["status"] == "success":
                logger.info(f"Message sent successfully to {recipient}")
                return result
            else:
                logger.error(f"Failed to send message: {result['error']}")
                return None
                
        except Exception as e:
            logger.error(f"Error in message transmission: {e}")
            raise
```

## Dependencies

Required packages:
```
cryptography>=41.0.0
pyjwt>=2.8.0
requests>=2.31.0
aiohttp>=3.9.0
```

## Support

For issues and questions:
1. Check the documentation above
2. Run tests with debug logging
3. Review error messages and logs
4. Open an issue with details

## License

MIT License - See LICENSE file for details 
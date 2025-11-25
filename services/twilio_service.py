import os
from twilio.rest import Client

# Global client variable
_client = None

def _get_client():
    """
    Lazy initialization of Twilio client.
    Only creates the client when actually needed.
    """
    global _client
    
    if _client is not None:
        return _client
    
    # Load environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    api_key_sid = os.getenv('TWILIO_API_KEY_SID')
    api_key_secret = os.getenv('TWILIO_API_KEY_SECRET')
    
    # Initialize Twilio Client
    # Use API Key if available, otherwise fallback to Auth Token
    if api_key_sid and api_key_secret and account_sid:
        _client = Client(api_key_sid, api_key_secret, account_sid)
        print("Twilio client initialized with API Key")
    elif account_sid and auth_token:
        _client = Client(account_sid, auth_token)
        print("Twilio client initialized with Auth Token")
    else:
        print("Warning: Twilio credentials not found. Message sending will fail.")
        return None
    
    return _client

def send_whatsapp_message(to_number, body_text):
    """
    Sends a WhatsApp message to the specified number.
    
    Args:
        to_number (str): The recipient's phone number (e.g., 'whatsapp:+821012345678').
        body_text (str): The content of the message.
        
    Returns:
        str: The SID of the sent message, or None if failed.
    """
    client = _get_client()
    
    if not client:
        print("Error: Twilio client not initialized. Check environment variables.")
        return None
    
    twilio_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    if not twilio_number:
        print("Error: TWILIO_WHATSAPP_NUMBER not set.")
        return None
    
    try:
        message = client.messages.create(
            from_=twilio_number,
            body=body_text,
            to=to_number
        )
        print(f"Message sent to {to_number}: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Error sending message to {to_number}: {e}")
        return None


import os
from twilio.rest import Client

# Load environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
api_key_sid = os.getenv('TWILIO_API_KEY_SID')
api_key_secret = os.getenv('TWILIO_API_KEY_SECRET')
twilio_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Initialize Twilio Client
# Use API Key if available, otherwise fallback to Auth Token
if api_key_sid and api_key_secret:
    client = Client(api_key_sid, api_key_secret, account_sid)
else:
    client = Client(account_sid, auth_token)

def send_whatsapp_message(to_number, body_text):
    """
    Sends a WhatsApp message to the specified number.
    
    Args:
        to_number (str): The recipient's phone number (e.g., 'whatsapp:+821012345678').
        body_text (str): The content of the message.
        
    Returns:
        str: The SID of the sent message, or None if failed.
    """
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

import os
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from services.twilio_service import send_whatsapp_message
from services.gsheets_service import gsheets_service
from services.openai_service import find_best_faq, generate_fallback_response
from services.session_service import get_user_session, update_user_session

app = Flask(__name__)

# Load FAQ data once at startup
print("Loading FAQ data from Google Sheets...")
FAQ_DATA = gsheets_service.load_faq_data()
print(f"Loaded {len(FAQ_DATA)} FAQ entries.")

@app.route('/')
def home():
    return "JBNU WhatsApp Chatbot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming WhatsApp messages via Twilio Webhook.
    """
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    if not sender or not incoming_msg:
        return "OK", 200
    
    print(f"Received message from {sender}: {incoming_msg}")
    
    # Get user session
    session = get_user_session(sender)
    
    # Process message and generate response
    response_text = process_message(incoming_msg, session)
    
    # Update session
    update_user_session(sender, last_message=incoming_msg)
    
    # Send response
    send_whatsapp_message(sender, response_text)
    
    return "OK", 200

def process_message(message, session):
    """
    Process the user's message and generate an appropriate response.
    
    Args:
        message (str): The user's message.
        session (dict): The user's session data.
        
    Returns:
        str: The response to send to the user.
    """
    # Try to find a matching FAQ
    match = find_best_faq(message, FAQ_DATA, threshold=0.7)
    
    if match:
        # Return the FAQ answer
        return match['answer']
    else:
        # Generate a fallback response using GPT
        return generate_fallback_response(message)

if __name__ == '__main__':
    app.run(debug=True, port=5002)

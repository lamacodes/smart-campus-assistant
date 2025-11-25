# In-Memory User Session Management

# Simple dictionary to store user sessions
# Key: phone number (e.g., 'whatsapp:+821012345678')
# Value: dict with 'role', 'last_message', 'timestamp', etc.
user_sessions = {}

def get_user_session(phone_number):
    """
    Get or create a user session.
    
    Args:
        phone_number (str): The user's phone number.
        
    Returns:
        dict: The user's session data.
    """
    if phone_number not in user_sessions:
        user_sessions[phone_number] = {
            'role': None,  # 'student', 'professor', 'partner'
            'last_message': '',
            'message_count': 0
        }
    
    return user_sessions[phone_number]

def update_user_session(phone_number, **kwargs):
    """
    Update a user's session data.
    
    Args:
        phone_number (str): The user's phone number.
        **kwargs: Key-value pairs to update in the session.
    """
    session = get_user_session(phone_number)
    session.update(kwargs)
    session['message_count'] += 1

def clear_all_sessions():
    """Clear all user sessions (useful for testing)."""
    global user_sessions
    user_sessions = {}

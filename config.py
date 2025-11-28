import os

# OpenAI Configuration
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_TEMPERATURE = 0.3

# University & Contact Information
UNIVERSITY_NAME = "UNIV"
OFFICE_EMAIL = "exchange@example.com"

# FAQ Configuration
FAQ_MATCH_THRESHOLD = 0.7

# System Prompts
SYSTEM_PROMPT = f"You are a helpful assistant for {UNIVERSITY_NAME} International Office. If you don't know the answer, politely say so and suggest contacting the office at {OFFICE_EMAIL}."

# Fallback Messages
FALLBACK_ERROR_MESSAGE = f"I'm sorry, I couldn't process your question at the moment. Please contact our office at {OFFICE_EMAIL} for assistance."
FALLBACK_NO_MATCH_MESSAGE = f"I'm sorry, I couldn't find an answer to your question. Please contact our office at {OFFICE_EMAIL} for assistance."

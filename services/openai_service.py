import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_embedding(text, model="text-embedding-3-small"):
    """
    Generate an embedding vector for the given text.
    
    Args:
        text (str): The text to embed.
        model (str): The embedding model to use.
        
    Returns:
        list: The embedding vector.
    """
    try:
        text = text.replace("\n", " ")
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1 (list): First vector.
        vec2 (list): Second vector.
        
    Returns:
        float: Cosine similarity score (0 to 1).
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    
    return dot_product / (norm_vec1 * norm_vec2)

def find_best_faq(user_query, faq_list, threshold=0.7):
    """
    Find the best matching FAQ entry for a user query using embeddings.
    
    Args:
        user_query (str): The user's question.
        faq_list (list): List of FAQ dictionaries with 'question', 'answer', etc.
        threshold (float): Minimum similarity score to consider a match.
        
    Returns:
        dict or None: The best matching FAQ entry, or None if no match above threshold.
    """
    # Generate embedding for user query
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return None
    
    best_match = None
    best_score = 0.0
    
    for faq in faq_list:
        # Generate embedding for FAQ question
        faq_question = faq.get('question', '')
        if not faq_question:
            continue
            
        faq_embedding = get_embedding(faq_question)
        if not faq_embedding:
            continue
        
        # Calculate similarity
        similarity = cosine_similarity(query_embedding, faq_embedding)
        
        if similarity > best_score:
            best_score = similarity
            best_match = faq
    
    # Return match only if above threshold
    if best_score >= threshold:
        print(f"Best match found with score {best_score:.2f}: {best_match.get('question')}")
        return best_match
    else:
        print(f"No match found above threshold {threshold}. Best score was {best_score:.2f}")
        return None

def generate_fallback_response(user_query):
    """
    Generate a helpful fallback response using GPT when no FAQ match is found.
    
    Args:
        user_query (str): The user's question.
        
    Returns:
        str: A helpful response or escalation message.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for JBNU International Office. If you don't know the answer, politely say so and suggest contacting the office at exchange@jbnu.ac.kr."},
                {"role": "user", "content": user_query}
            ],
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating fallback response: {e}")
        return "I'm sorry, I couldn't find an answer to your question. Please contact our office at exchange@jbnu.ac.kr for assistance."

from services.openai_service import get_embedding, find_best_faq, generate_fallback_response
from services.gsheets_service import gsheets_service
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai():
    print("Testing OpenAI service...")
    
    # Load FAQ data
    faq_data = gsheets_service.load_faq_data()
    
    if not faq_data:
        print("No FAQ data loaded. Please check Google Sheets setup.")
        return
    
    # Test queries
    test_queries = [
        "When is the deadline?",
        "How much does the dorm cost?",
        "What is the weather like?",  # Should not match
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        # Find best match
        match = find_best_faq(query, faq_data, threshold=0.7)
        
        if match:
            print(f"✅ Match found!")
            print(f"Question: {match['question']}")
            print(f"Answer: {match['answer']}")
        else:
            print(f"❌ No match found. Generating fallback...")
            fallback = generate_fallback_response(query)
            print(f"Fallback: {fallback}")

if __name__ == "__main__":
    test_openai()

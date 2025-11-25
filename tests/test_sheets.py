from services.gsheets_service import gsheets_service
import os
from dotenv import load_dotenv

# Load environment variables manually if running standalone
load_dotenv()

def test_sheets():
    print("Testing Google Sheets connection...")
    
    # Check if env vars are loaded
    if not os.getenv('GOOGLE_SHEET_ID'):
        print("Error: GOOGLE_SHEET_ID is not set in .env")
        return
    
    data = gsheets_service.load_faq_data()
    
    if data:
        print("\nSuccessfully loaded data!")
        print(f"First entry: {data[0]}")
        print(f"Total entries: {len(data)}")
    else:
        print("\nFailed to load data or sheet is empty.")

if __name__ == "__main__":
    test_sheets()

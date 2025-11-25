import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Scopes required for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class GoogleSheetsService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.creds_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', 'credentials.json')
        
        self._authenticate()

    def _authenticate(self):
        """Authenticates with Google Sheets API using service account credentials."""
        # Try to load from environment variable first (for Railway deployment)
        creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
        
        if creds_json:
            try:
                # Parse JSON from environment variable
                creds_info = json.loads(creds_json)
                self.creds = Credentials.from_service_account_info(
                    creds_info, scopes=SCOPES)
                self.service = build('sheets', 'v4', credentials=self.creds)
                print("Successfully authenticated with Google Sheets API (from env var).")
                return
            except Exception as e:
                print(f"Error loading credentials from environment variable: {e}")
        
        # Fallback to file-based credentials (for local development)
        if os.path.exists(self.creds_file):
            try:
                self.creds = Credentials.from_service_account_file(
                    self.creds_file, scopes=SCOPES)
                self.service = build('sheets', 'v4', credentials=self.creds)
                print("Successfully authenticated with Google Sheets API (from file).")
            except Exception as e:
                print(f"Error loading credentials from file: {e}")
        else:
            print(f"Credentials file not found: {self.creds_file}")


    def load_faq_data(self):
        """
        Fetches FAQ data from the Google Sheet.
        Assumes the first row is the header.
        Returns a list of dictionaries.
        """
        if not self.service:
            print("Google Sheets service is not initialized.")
            return []

        try:
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id,
                                        range='A:D').execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return []

            # Parse headers and data
            headers = [h.lower() for h in values[0]] # category, question, answer, keywords
            faq_list = []
            
            for row in values[1:]:
                # Ensure row has enough columns (pad with empty strings if needed)
                while len(row) < len(headers):
                    row.append("")
                
                entry = dict(zip(headers, row))
                faq_list.append(entry)

            print(f"Loaded {len(faq_list)} FAQ entries from Google Sheets.")
            return faq_list

        except Exception as e:
            print(f"An error occurred while fetching data: {e}")
            return []

# Singleton instance for easy import
gsheets_service = GoogleSheetsService()

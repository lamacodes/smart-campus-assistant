# JBNU WhatsApp Chatbot

An AI‑powered WhatsApp chatbot for JBNU International Office to automatically answer student inquiries.

## Features
- 24/7 automated FAQ responses
- AI‑powered semantic search using OpenAI embeddings
- Google Sheets integration for easy FAQ management
- Fallback GPT responses for unmatched questions
- In‑memory user session management

## Tech Stack
- **Backend:** Python Flask
- **Messaging:** Twilio WhatsApp API
- **AI:** OpenAI (Embeddings + GPT‑3.5‑turbo)
- **Data:** Google Sheets API
- **Deployment:** Railway

## Setup

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
Required variables:
- `OPENAI_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_API_KEY_SID` and `TWILIO_API_KEY_SECRET`
- `TWILIO_WHATSAPP_NUMBER`
- `GOOGLE_SHEET_ID`
- `GOOGLE_CREDENTIALS_JSON` (full JSON content of the service‑account file)

### 3. Add Google Service Account Credentials
Place your `credentials.json` file in the project root directory (or paste its JSON into `GOOGLE_CREDENTIALS_JSON`).

### 4. Run Locally
```bash
python app.py
```
The server will start on `http://localhost:5002`.

## Deployment to Railway
1. Push your code to GitHub (ensure `.env` and `credentials.json` are in `.gitignore`).
2. Connect your GitHub repo to Railway.
3. Add the environment variables in the Railway dashboard (same as above).
4. Railway will automatically detect the `Procfile` and deploy.
5. **Deployment URL:** `https://web-production-4871a.up.railway.app`

## Testing
### Test Google Sheets Connection
```bash
python test_sheets.py
```
### Test OpenAI Service
```bash
python test_openai.py
```

## Project Structure
```
chatbot-wechat/
├── app.py                      # Main Flask application
├── services/
│   ├── twilio_service.py       # WhatsApp messaging
│   ├── gsheets_service.py      # FAQ data loader
│   ├── openai_service.py       # AI embeddings & search
│   └── session_service.py      # User session management
├── docs/                       # Documentation
├── tests/                      # Test scripts
│   ├── test_openai.py
│   └── test_sheets.py
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment config
└── .env.example                # Environment template
```

## License
MIT

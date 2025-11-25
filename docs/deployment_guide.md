# Deployment Guide

## Railway Deployment

1. **Initialize Git Repository**
   ```bash
   cd /Users/uijungwon/Downloads/project/chatbot-wechat
   git init
   git add .
   git commit -m "Initial commit: JBNU WhatsApp Chatbot"
   ```

2. **Create GitHub Repository**
   - Go to https://github.com/new
   - Create a new repository (e.g., `jbnu-whatsapp-chatbot`). Do NOT initialize with a README.
   - Copy the repository URL.

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/jbnu-whatsapp-chatbot.git
   git branch -M main
   git push -u origin main
   ```

4. **Deploy to Railway**
   - Open the Railway dashboard (https://railway.app/dashboard).
   - Click **New Project** → **Deploy from GitHub repo**.
   - Select your `jbnu-whatsapp-chatbot` repository.
   - Railway will detect the `Procfile` and start the deployment.

## Environment Variables (Railway)

Add the following variables in the **Variables** tab of your Railway project:

- **OpenAI**
  ```
  OPENAI_API_KEY=sk-...
  ```
- **Twilio** (API‑Key mode)
  ```
  TWILIO_ACCOUNT_SID=AC...
  TWILIO_API_KEY_SID=SK...
  TWILIO_API_KEY_SECRET=...
  TWILIO_WHATSAPP_NUMBER=whatsapp:+821033812330
  ```
- **Google Sheets**
  ```
  GOOGLE_SHEET_ID=...
  ```
- **Google Credentials** (full JSON on a single line)
  ```
  GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
  ```

> **Important:** Paste the entire JSON content of `credentials.json` as a single line without line‑breaks.

After saving the variables, Railway will automatically redeploy the service.

## Twilio Webhook Setup

1. Log in to the Twilio Console (https://console.twilio.com/).
2. Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**.
3. In the **Sandbox settings**, locate the **"When a message comes in"** section.
4. Set the webhook URL to:
   ```
   https://web-production-4871a.up.railway.app/webhook
   ```
5. Choose **POST** as the method and click **Save**.

## Testing

- Send a WhatsApp message to your Twilio Sandbox number (e.g., `whatsapp:+821033812330`).
- Try: "When is the deadline?".
- The bot should reply with the correct FAQ answer (**2025년 11월 28일입니다.**).

## Troubleshooting

- **Railway logs:** Project → Deployments → View logs.
- **Twilio logs:** Console → Monitor → Logs.
- Ensure all environment variables are correctly set and contain no extra whitespace or line‑breaks.

---

*This guide consolidates the previous Railway deployment, environment‑variable, and Twilio webhook documentation into a single reference.*

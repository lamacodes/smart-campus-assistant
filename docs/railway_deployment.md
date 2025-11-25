# Railway Deployment Guide

## Step 1: Initialize Git Repository
```bash
cd /Users/uijungwon/Downloads/project/chatbot-wechat
git init
git add .
git commit -m "Initial commit: JBNU WhatsApp Chatbot"
```

## Step 2: Create GitHub Repository
1. Go to [GitHub](https://github.com/new)
2. Create a new repository (e.g., `jbnu-whatsapp-chatbot`)
3. **Do NOT** initialize with README (we already have one)
4. Copy the repository URL

## Step 3: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/jbnu-whatsapp-chatbot.git
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Railway
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `jbnu-whatsapp-chatbot` repository
5. Railway will automatically detect `Procfile` and start deploying

## Step 5: Set Environment Variables in Railway
Click on your project → **Variables** tab → Add the following:

### Required Variables
```
OPENAI_API_KEY=sk-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_API_KEY_SID=SK...
TWILIO_API_KEY_SECRET=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GOOGLE_SHEET_ID=...
```

### Google Credentials (Important!)
**Option 1: Environment Variable (Recommended)**
1. Open your local `credentials.json` file
2. Copy the **entire JSON content** (it should start with `{"type":"service_account",...}`)
3. In Railway Variables, add:
   - Name: `GOOGLE_CREDENTIALS_JSON`
   - Value: Paste the entire JSON content

**Option 2: File-based (Alternative)**
If you prefer, you can also set:
```
GOOGLE_SHEETS_CREDENTIALS_JSON=credentials.json
```
And upload the file via Railway's file storage (more complex).

## Step 6: Get Railway Deployment URL
1. After deployment completes, Railway will show your app URL
2. Copy the URL (e.g., `https://your-app.up.railway.app`)

## Step 7: Configure Twilio Webhook
1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. In the **Sandbox settings**, find **"When a message comes in"**
4. Set the webhook URL to: `https://your-app.up.railway.app/webhook`
5. Method: **POST**
6. Save

## Step 8: Test!
1. Send a WhatsApp message to your Twilio Sandbox number
2. Try: "When is the deadline?"
3. The bot should respond with the FAQ answer!

## Troubleshooting
- **Check Railway Logs**: Click on your project → **Deployments** → View logs
- **Test locally first**: Run `python app.py` to ensure everything works
- **Verify environment variables**: Make sure all variables are set correctly in Railway

## Next Steps
- Monitor usage in OpenAI and Twilio dashboards
- Add more FAQs to your Google Sheet
- Consider upgrading to Twilio production number for real users

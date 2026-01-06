# Streamlit Cloud Deployment Guide

This guide explains how to securely deploy the Architect Blueprint application to Streamlit Cloud.

## 🔒 Security Overview

Your API keys are secured using **Streamlit Secrets Management**:
- ✅ Secrets stored on Streamlit Cloud (NOT in your repository)
- ✅ Encrypted and only accessible to your app
- ✅ Never exposed in logs or error messages
- ✅ Can be updated without redeploying

## 📋 Prerequisites

1. **GitHub Account** with your repository
2. **Streamlit Cloud Account** (free tier available)
3. **API Keys** for at least one LLM provider:
   - DeepSeek (Recommended): https://platform.deepseek.com/
   - OpenAI: https://platform.openai.com/api-keys
   - Groq: https://console.groq.com/
   - Kimi: https://platform.moonshot.cn/

## 🚀 Deployment Steps

### Step 1: Push to GitHub

Your code is already pushed to:
```
https://github.com/somepalli/architect-blueprint
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io/
   - Click "New app" button

2. **Connect Your Repository**:
   - Repository: `somepalli/architect-blueprint`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Wait for deployment** (~2-3 minutes)

### Step 3: Configure Secrets (CRITICAL)

1. **Access Secrets Panel**:
   - Go to your app dashboard: https://share.streamlit.io/
   - Click on your app
   - Click Settings (⚙️ icon) → "Secrets"

2. **Add Your API Keys**:

Copy and paste this template, replacing with your actual keys:

```toml
# LLM Provider API Keys (add only the ones you have)
DEEPSEEK_API_KEY = "sk-your-actual-deepseek-key"
# OPENAI_API_KEY = "sk-your-actual-openai-key"
# GROQ_API_KEY = "gsk-your-actual-groq-key"
# MOONSHOT_API_KEY = "sk-your-actual-kimi-key"

# Configuration
DEFAULT_PROVIDER = "deepseek"
MAX_TOKENS = "4096"
TEMPERATURE = "0.3"
```

3. **Click "Save"** - Your app will automatically restart with the new secrets

### Step 4: Test Your Deployment

1. Visit your app URL (something like):
   ```
   https://your-app-name.streamlit.app/
   ```

2. Test the blueprint generation:
   - Select your provider (the one you added the API key for)
   - Enter a sample SaaS idea
   - Click "Generate Blueprint"
   - Verify it works without errors

## 🔐 Security Best Practices

### ✅ DO:
- Store API keys in Streamlit Secrets (NOT in code or .env)
- Use different API keys for development and production
- Rotate keys periodically
- Monitor API usage on provider dashboards
- Use DeepSeek for cost savings (97% cheaper)

### ❌ DON'T:
- Never commit `.env` file to git (already in .gitignore)
- Never hardcode API keys in Python files
- Never share your secrets.toml file
- Never expose secrets in logs or error messages

## 💰 Cost Management

### Recommended Setup for Public Deployment:

**Option 1: Use Your Own Keys (Current Setup)**
- Add your API keys to Streamlit Secrets
- Monitor usage on provider dashboards
- Set up billing alerts
- Estimated cost with DeepSeek: $0.01-0.02 per blueprint

**Option 2: Let Users Provide Their Own Keys**
- See "User-Provided Keys" section below
- Zero cost to you
- Users input their own API keys in the UI

### Setting Up Usage Limits:

1. **DeepSeek** (https://platform.deepseek.com/):
   - Go to Settings → Billing
   - Set monthly spending limit
   - Enable email alerts

2. **OpenAI** (https://platform.openai.com/):
   - Go to Settings → Limits
   - Set monthly budget and usage limits
   - Configure email notifications

## 🔄 Updating Your Deployment

### Update Code:
```bash
git add .
git commit -m "Your update message"
git push origin main
```
Streamlit Cloud will automatically redeploy.

### Update Secrets:
1. Go to your app on Streamlit Cloud
2. Settings → Secrets
3. Edit the secrets
4. Click "Save" (app will restart automatically)

## 🚨 Troubleshooting

### App Not Working?

1. **Check Secrets Configuration**:
   - Go to Settings → Secrets
   - Verify API keys are correctly formatted
   - Ensure no extra quotes or spaces

2. **Check Logs**:
   - Click "Manage app" → "Logs"
   - Look for error messages about API keys

3. **Common Issues**:
   - `KeyError: 'DEEPSEEK_API_KEY'` → Add the key to Secrets
   - `Invalid API key` → Check key is correct on provider dashboard
   - `Rate limit exceeded` → Wait or increase provider limits

### App Running But Errors During Generation?

1. **Check Provider Status**:
   - Verify API key is valid
   - Check provider dashboard for outages
   - Ensure you have credits/billing enabled

2. **Try Different Provider**:
   - Switch from Groq (has issues) to DeepSeek
   - Add multiple provider keys as fallback

## 📊 Monitoring

### Track Usage:
1. **Streamlit Cloud Analytics**:
   - View app usage at https://share.streamlit.io/
   - Monitor active users and sessions

2. **LLM Provider Dashboards**:
   - DeepSeek: https://platform.deepseek.com/usage
   - OpenAI: https://platform.openai.com/usage
   - Groq: https://console.groq.com/usage
   - Kimi: https://platform.moonshot.cn/usage

### Set Up Alerts:
- Configure billing alerts on each provider
- Set up email notifications for unusual usage
- Monitor costs daily initially

## 🔧 Advanced: User-Provided API Keys

If you want users to provide their own API keys (zero cost to you):

1. **Update `input_form.py`** to add API key input field
2. **Pass user key to agents** instead of settings.py
3. **Add warning** about key security

Example implementation available in the codebase - ask if you need help setting this up.

## 📞 Support

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Secrets Management**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **GitHub Issues**: https://github.com/somepalli/architect-blueprint/issues

## 🎉 Your App

Your deployed app: **https://architect-blueprintgit-4v2sswlh5a4nvugapepusv.streamlit.app/**

Enjoy building amazing SaaS blueprints! 🚀

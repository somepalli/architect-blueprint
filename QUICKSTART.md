# Quick Start Guide

Get your Micro-SaaS Architect up and running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup Steps

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd Architect_Blueprint

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-api-key-here
```

On Windows, you can use:
```bash
copy .env.example .env
notepad .env
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## First Blueprint

1. **Enter your idea**: Describe your SaaS business in detail
   - Example: "A task management app for remote teams with Kanban boards, time tracking, and Slack integration"

2. **Select detail level**:
   - **High-Level**: Quick overview (5-10 min)
   - **Detailed**: Comprehensive specs (recommended, 3-5 min)
   - **Production-Ready**: Full implementation guide (5-10 min)

3. **Choose platform**: Select your deployment target (AWS, GCP, Azure, etc.)

4. **Generate**: Click "Generate Blueprint" and watch the magic happen!

## What to Expect

The AI agents will:
1. ✅ Analyze your requirements (30 sec)
2. ✅ Design database schema (1 min)
3. ✅ Create API endpoints (1 min)
4. ✅ Plan frontend architecture (1 min)
5. ✅ Generate deployment plan (1 min)

**Total Time**: 2-5 minutes depending on complexity and detail level

## Troubleshooting

### "OPENAI_API_KEY is not set"
- Make sure your `.env` file exists and contains your API key
- Verify the key starts with `sk-`
- Restart the application after setting the key

### "Module not found" errors
- Ensure you activated the virtual environment
- Run `pip install -r requirements.txt` again

### Slow generation
- This is normal! Complex blueprints take 3-5 minutes
- GPT-4 is thorough but slower than GPT-3.5
- Your API key's rate limits may affect speed

### Diagrams not showing
- Check your browser console for errors
- Try refreshing the page
- Ensure JavaScript is enabled

## Cost Estimate

- **High-Level**: ~$0.10-0.20 per blueprint
- **Detailed**: ~$0.30-0.50 per blueprint
- **Production-Ready**: ~$0.50-1.00 per blueprint

*Based on GPT-4-turbo pricing as of 2024*

## Next Steps

1. Export your blueprint (Markdown or JSON)
2. Share with your team
3. Use as a foundation for development planning
4. Iterate and refine your idea

## Support

- Check the main [README.md](README.md) for full documentation
- Review the implementation plan in `.claude/plans/`
- Open an issue if you encounter problems

Happy architecting! 🏗️

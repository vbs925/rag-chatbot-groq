# Quick Start Commands

## Setup (First Time Only)

```bash
# Navigate to project
cd /Users/varunbharadwaj/.gemini/antigravity/scratch/rag-chatbot-groq

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Then edit .env and add your Groq API key
```

## Running the App

```bash
# Navigate to project (if not already there)
cd /Users/varunbharadwaj/.gemini/antigravity/scratch/rag-chatbot-groq

# Activate virtual environment
source venv/bin/activate

# Run the chatbot
streamlit run app.py
```

## Testing Components

```bash
# Make sure virtual environment is activated
python test_components.py
```

## Get Groq API Key

Visit: https://console.groq.com/
1. Sign up for free account
2. Go to API Keys section
3. Create new API key
4. Copy and paste into .env file

## Deactivate Virtual Environment

```bash
deactivate
```

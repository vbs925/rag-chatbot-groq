# ✅ Setup Complete - Get Your Groq API Key Now!

## 🎯 Next Step: Get Your FREE Groq API Key

Your chatbot is installed and ready! You just need a Groq API key to start chatting.

### Step 1: Get API Key (2 minutes)

1. **Visit**: [https://console.groq.com/](https://console.groq.com/)
2. **Sign up** with your email (it's FREE!)
3. **Go to "API Keys"** in the left sidebar
4. **Click "Create API Key"**
5. **Copy** your API key

### Step 2: Configure API Key

```bash
# Create .env file
cp .env.example .env

# Open and edit the .env file
nano .env
```

**Add your API key** to the `.env` file:
```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Save**: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

### Step 3: Run the Chatbot! 🚀

```bash
streamlit run app.py
```

That's it! The app will open in your browser automatically.

---

## 📖 How to Use

1. **Upload a Document**: Click "Browse files" in the sidebar, select a PDF or TXT file
2. **Process**: Click "Process Document" button
3. **Chat**: Ask questions about your document!

### Example Questions:
- "What is this document about?"
- "Summarize the main points"
- "What does it say about [topic]?"

---

## 🔧 Common Commands

### Start the Chatbot
```bash
cd /Users/varunbharadwaj/rag-chatbot-groq
source venv/bin/activate  # Activate virtual environment
streamlit run app.py
```

### Stop the Chatbot
Press `Ctrl+C` in the terminal

### Deactivate Virtual Environment
```bash
deactivate
```

---

## 🎉 You're All Set!

Get your Groq API key from [console.groq.com](https://console.groq.com/) and start chatting with your documents!

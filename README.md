---
title: Legal Advisor Chatbot
emoji: ⚖️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.1.0
app_file: app.py
pinned: false
license: mit
---

# ⚖️ Legal Advisor Chatbot

A professional AI-powered legal advisor chatbot built with Gradio and powered by GROQ's Llama3 model. This chatbot provides general legal information and guidance across multiple legal domains.

## 🎯 Features

- **Multi-Domain Legal Expertise**: Covers Contract Law, Employment Law, Property Law, Criminal Law, Family Law, Intellectual Property, Tort Law, Business Law, and Civil Rights
- **Customizable Responses**: 
  - Legal topic focus dropdown
  - Response length control (Brief/Medium/Detailed)
  - Creativity slider for response style
- **Professional Interface**: Clean, user-friendly Gradio interface
- **Conversation History**: Maintains context throughout the conversation

## 🚀 How to Use

1. **Get Your GROQ API Key**:
   - Visit https://console.groq.com
   - Sign up and get your API key

2. **Set Up on Hugging Face Spaces**:
   - Create a new Gradio Space
   - Upload `app.py` and `requirements.txt`
   - Go to Settings > Secrets
   - Add `GROQ_API_KEY` with your API key value

3. **Start Chatting**:
   - Select a legal topic from the dropdown (optional)
   - Adjust response length and creativity settings
   - Ask your legal questions!

## 📋 Example Questions

- "What is a contract?"
- "Tell me about employment rights"
- "What should I do if I'm arrested?"
- "Explain property law basics"
- "What is intellectual property?"

## ⚠️ Important Disclaimer

**This chatbot provides general legal information only and does NOT constitute legal advice.**

- Always consult a qualified attorney for specific legal matters
- Laws vary by jurisdiction
- This is an educational tool for learning purposes
- Do not rely solely on chatbot responses for legal decisions

## 🛠️ Technical Details

- **Framework**: Gradio 6.0+
- **LLM**: GROQ API (llama-3.3-70b-versatile)
- **Language**: Python 3.8+

## 📝 Customization

The chatbot's personality and expertise are defined in the `SYSTEM_PROMPT` variable in `app.py`. You can customize:
- Chatbot name and personality
- Legal domains covered
- Response style and tone
- Disclaimer messages

## 📄 License

MIT License - Educational use

---

**Built for IDS Chatbot Tutorial & Lab Task**

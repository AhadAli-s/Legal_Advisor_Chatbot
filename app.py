import gradio as gr
import os
import requests


GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a professional and knowledgeable Legal Advisor chatbot named LexBot.
You provide general legal information and guidance to users in a clear, helpful, and accessible manner.

Your personality:
- Professional yet approachable
- Clear and concise in explanations
- Empathetic and understanding
- Always includes appropriate legal disclaimers

Your expertise covers:
- Contract Law (agreements, breaches, obligations)
- Employment Law (rights, discrimination, termination, workplace rights)
- Property Law (real estate, landlord-tenant, ownership)
- Criminal Law (rights, procedures, charges)
- Family Law (divorce, custody, adoption, women's rights)
- Intellectual Property (copyright, patents, trademarks)
- Tort Law (negligence, personal injury, damages)
- Business Law (corporations, LLCs, partnerships)
- Civil Rights and Gender Equality (discrimination, equal rights, workplace equality)

IMPORTANT GUIDELINES:
- Provide general legal information only, not specific legal advice
- Always remind users that laws vary by jurisdiction
- Encourage users to consult qualified attorneys for specific cases
- Be clear that you cannot replace professional legal counsel
- Use simple language to explain complex legal concepts
- If asked about something outside your knowledge, politely redirect to relevant legal topics
- When discussing women's rights or gender equality, provide comprehensive information about legal protections, workplace rights, discrimination laws, and relevant legislation"""


def query_groq(message, chat_history, legal_topic="General", response_length="Medium", temperature=0.7):
    """Query GROQ API with the message and chat history"""
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not set. Please set your API key in environment variables."
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build system prompt with topic context
    topic_context = ""
    if legal_topic != "General":
        topic_context = f"\n\nCurrent focus area: {legal_topic}. Provide information relevant to this legal domain."
    
    length_instruction = ""
    if response_length == "Brief":
        length_instruction = " Keep your response concise (2-3 sentences)."
    elif response_length == "Detailed":
        length_instruction = " Provide a comprehensive explanation with examples."
    else:
        length_instruction = " Provide a balanced explanation (3-5 sentences)."
    
    enhanced_system_prompt = SYSTEM_PROMPT + topic_context + length_instruction
    
    messages = [{"role": "system", "content": enhanced_system_prompt}]
    
    # Add chat history - handle dictionary format for Gradio 5.x
    if chat_history:
        for entry in chat_history:
            if isinstance(entry, dict):
                messages.append(entry)
    
    # Add current message
    if message and isinstance(message, str) and message.strip():
        messages.append({"role": "user", "content": message.strip()})
    
    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "temperature": temperature
            },
            timeout=30
        )
        
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            disclaimer = "\n\n⚠️ **Disclaimer:** This is general legal information only and does not constitute legal advice. Always consult a qualified attorney for specific legal matters."
            return reply + disclaimer
        else:
            error_text = response.text
            try:
                error_json = response.json()
                error_text = error_json.get("error", {}).get("message", error_text)
            except:
                pass
            return f"Error {response.status_code}: {error_text}"
    except Exception as e:
        return f"Error connecting to GROQ API: {str(e)}. Please check your API key and internet connection."


# Create Gradio interface with modern design
with gr.Blocks(title="Legal Advisor Chatbot - LexBot") as demo:
    # Header Section
    with gr.Row():
        gr.HTML("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-size: 2.5em;">⚖️ LexBot</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1em;">Your AI Legal Advisor - Powered by GROQ</p>
        </div>
        """)
    
    # Main Content Area
    with gr.Row():
        # Left Column - Chat Interface
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="",
                height=600,
                show_label=False
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="",
                    placeholder="Ask your legal question here... (e.g., What is a contract?, Explain employment law...)",
                    lines=1,
                    scale=5,
                    show_label=False,
                    container=False,
                    submit_btn=True
                )
                submit_btn = gr.Button(
                    "Send 📤",
                    variant="primary",
                    scale=1,
                    size="lg",
                    min_width=100
                )
            
            # Quick Action Buttons
            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary", scale=1)
                gr.HTML("<div style='text-align: center; color: #666; font-size: 0.9em; padding: 10px;'>Press Enter or click Send to ask your question</div>", scale=2)
        
        # Right Column - Settings
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Settings")
            
            legal_topic = gr.Dropdown(
                choices=[
                    "General",
                    "Employment Law",
                    "Family Law",
                    "Contract Law",
                    "Property Law",
                    "Criminal Law",
                    "Intellectual Property",
                    "Tort Law",
                    "Business Law",
                    "Civil Rights"
                ],
                value="General",
                label="📚 Legal Topic Focus",
                info="Select a legal area to focus the conversation"
            )
            
            response_length = gr.Radio(
                choices=["Brief", "Medium", "Detailed"],
                value="Medium",
                label="📏 Response Length",
                info="Choose how detailed you want the response"
            )
            
            temperature_slider = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.7,
                step=0.1,
                label="🎨 Response Style",
                info="Lower = more focused | Higher = more creative"
            )
            
            gr.Markdown("---")
            gr.Markdown("""
            ### 💡 Tips
            - Be specific with your questions
            - Select a legal topic for focused answers
            - Adjust response length as needed
            - This provides general information only
            """)
    
    # Footer
    gr.Markdown("""
    ---
    <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; margin-top: 20px;">
        <p style="margin: 5px 0; color: #666;"><strong>⚠️ Important:</strong> This chatbot provides general legal information for educational purposes only.</p>
        <p style="margin: 5px 0; color: #666;">It does <strong>not</strong> constitute legal advice. For specific legal matters, please consult a qualified attorney.</p>
        <p style="margin: 5px 0; color: #999; font-size: 0.9em;">Laws vary by jurisdiction, and this information may not apply to your specific situation.</p>
    </div>
    """)
    
    # State management
    state = gr.State([])
    
    def respond_wrapper(message, history, topic, length, temp):
        """Wrapper to handle response and update both chatbot and state"""
        if not message or not message.strip():
            return history, history, ""
        
        # Get bot reply
        bot_reply = query_groq(message, history, topic, length, temp)
        
        # Create new messages in dictionary format (Gradio 5.x requirement)
        new_messages = [
            {"role": "user", "content": message},
            {"role": "assistant", "content": bot_reply}
        ]
        
        # Append to existing history
        new_history = history + new_messages
        
        return new_history, new_history, ""  # Return empty string to clear input
    
    # Connect events
    msg.submit(
        respond_wrapper,
        inputs=[msg, state, legal_topic, response_length, temperature_slider],
        outputs=[chatbot, state, msg]
    )
    
    submit_btn.click(
        respond_wrapper,
        inputs=[msg, state, legal_topic, response_length, temperature_slider],
        outputs=[chatbot, state, msg]
    )
    
    clear_btn.click(
        lambda: ([], []),
        None,
        outputs=[chatbot, state]
    )

if __name__ == "__main__":
    demo.launch(share=True)
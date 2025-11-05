from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64


load_dotenv(override=True)


def get_sheets_client():
    """Initialize Google Sheets client"""
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    credentials_file = 'credentials.json'
    
    if os.path.exists(credentials_file):
        print("✓ Using local credentials.json")
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, 
            scope
        )
    else:
        print("✓ Using HuggingFace environment credentials")
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDS")
        
        if not creds_json:
            raise ValueError("GOOGLE_SHEETS_CREDS not found in environment variables!")
        
        print(f"✓ Credentials JSON length: {len(creds_json)} characters")
        
        try:
            creds_dict = json.loads(creds_json)
            print(f"✓ Loaded credentials for: {creds_dict.get('client_email', 'unknown')}")
            print(f"✓ Project: {creds_dict.get('project_id', 'unknown')}")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse credentials JSON: {e}")
            raise ValueError("Invalid JSON in GOOGLE_SHEETS_CREDS!")
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict, 
            scope
        )
    
    return gspread.authorize(creds)

def record_user_details(email, name="Name not provided", notes="Not provided"):
    """Record user contact details to Google Sheets"""
    try:
        client = get_sheets_client()
        sheet_name = os.getenv("GOOGLE_SHEET_NAME", "ChatBot Contacts")
        spreadsheet = client.open(sheet_name)
        worksheet = spreadsheet.worksheet("Contacts")
        
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            email,
            notes
        ]
        
        worksheet.append_row(row, value_input_option='RAW')
        print(f"✓ Contact recorded: {name} ({email})")
        return {"status": "success", "message": f"Thank you! I've recorded your details. I'll get back to you at {email} soon."}
    
    except Exception as e:
        print(f"❌ Error recording contact: {e}")
        return {"status": "error", "message": "There was an error recording your details. Please try again."}

def record_unanswered_question(question, context=""):
    """Record questions the bot couldn't answer"""
    try:
        client = get_sheets_client()
        sheet_name = os.getenv("GOOGLE_SHEET_NAME", "ChatBot Contacts")
        spreadsheet = client.open(sheet_name)
        worksheet = spreadsheet.worksheet("Unanswered Questions")
        
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            question,
            context
        ]
        
        worksheet.append_row(row, value_input_option='RAW')
        print(f"✓ Unanswered question recorded")
        return {"status": "success", "message": "I've recorded your question for follow-up."}
    
    except Exception as e:
        print(f"❌ Error recording question: {e}")
        return {"status": "error", "message": "Error recording question."}



record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unanswered_question_json = {
    "name": "record_unanswered_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unanswered_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Antonis Bastoulis"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        readerCV = PdfReader("me/CV.pdf")
        self.CV = ""
        for page in readerCV.pages:
            text = page.extract_text()
            if text:
                self.CV += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"""You are {self.name}'s professional representative, answering questions about career, skills, and experience.
        You are an AI assistant representing {self.name}. Speak in first person as if you are {self.name}, using "I" and "my" when discussing his experience, skills, and background. However, if directly asked if you are AI or Antonis himself, be transparent that you're an AI assistant trained on his professional information.

        ## BOUNDARIES - Never Discuss:
        - Personal life (family, relationships, health, politics, religion)
        - Compensation details (past salaries, current income)
        - Why you left previous jobs
        - Negative comments about past employers/colleagues
        - Confidential project details or proprietary information
        - Personal contact info (home address, personal phone)

        ## How to Handle Restricted Topics:
        Redirect professionally: "I keep that private. Let me tell you about {self.name}'s expertise in [relevant area] instead."
        For salary questions: "Compensation is best discussed based on role requirements. What position interests you?"

        ## Available Information:
        ### Summary:
        {self.summary}
        ### LinkedIn Profile:
        {self.linkedin}
        ### CV:
        {self.CV}
        Stay in character as {self.name}'s professional representative. Be helpful within appropriate boundaries."""
        return system_prompt


    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    
    # Custom theme
    custom_theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
    ).set(
        body_background_fill="*neutral_50",
        button_primary_background_fill="*primary_600",
        button_primary_background_fill_hover="*primary_700",
    )
    
    with gr.Blocks(theme=custom_theme, title="Career Chatbot  ", css="""
        .header-container {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .header-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .header-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .example-box {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        .example-box p {
            margin: 0.5rem 0;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .example-box p:hover {
            transform: translateX(5px);
            color: #667eea;
        }
        footer {
            text-align: center;
            padding: 2rem;
            color: #666;
        }
    """) as demo:
        
        # Header
        gr.HTML("""
            <div class="header-container">
                <div class="header-title">Antonis Bastoulis</div>
                <div class="header-subtitle">
                    Naval Architect & Marine Engineer | M.Sc. in Artificial Intelligence & Deep Learning
                </div>
                <div style="font-size: 1rem; margin-top: 1rem; opacity: 0.85;">
                    AI Assistant • Ask me about my experience, projects, and expertise
                </div>
            </div>
        """)
        
        # Tabs for different sections
        with gr.Tabs():
            # Chat Tab
            with gr.TabItem("💬 Chat with Me"):
                with gr.Row():
                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(
                            label="Conversation",
                            height=500,
                            bubble_full_width=False,
                            show_copy_button=True,
                            type="messages"
                        )
                        
                        with gr.Row():
                            msg = gr.Textbox(
                                placeholder="Ask me about my experience, skills, projects...",
                                show_label=False,
                                scale=4,
                                container=False
                            )
                            submit_btn = gr.Button("Send", variant="primary", scale=1)
                        
                        with gr.Row():
                            clear = gr.Button("🔄 Clear Chat", size="sm")

            
            # About/FAQ Tab
            with gr.TabItem("ℹ️ About"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("""
                        ### About This Chatbot
                        
                        This AI assistant is trained on my professional profile and can answer questions about:
                        - 💼 Work experience and career history
                        - 🛠️ Technical skills and expertise
                        - 📁 Projects and achievements
                        - 🎓 Education and certifications
                        - 🎯 Career goals and interests
                        
                        ### How to Use
                        1. Ask any question about my professional background
                        2. If I can't answer something, it will be recorded for me to review
                        3. Want to connect? Simply tell the chatbot your name, email, and a message - I'll record your details and get back to you.
                        

                        ### Privacy & Data Protection
                        - Conversations are processed securely via OpenAI's API
                        - Contact information is only used to reach out to you
                        - Unanswered questions are recorded to improve responses
                        - No conversation history is permanently stored
                        
                        ---
                        """)
                
                gr.Markdown("### Connect With Me")
                gr.HTML("""
                    <div style="text-align: center; padding: 2rem;">
                        <a href="https://www.linkedin.com/in/antonisbast/" target="_blank" 
                           style="margin: 0 1rem; text-decoration: none; font-size: 1.1rem;">
                            🔗 LinkedIn
                        </a>
                        <a href="https://github.com/antonisbast" target="_blank" 
                           style="margin: 0 1rem; text-decoration: none; font-size: 1.1rem;">
                            💻 GitHub
                        </a>
                        <a href="mailto:antonisbast@gmail.com" 
                           style="margin: 0 1rem; text-decoration: none; font-size: 1.1rem;">
                            📧 Email
                        </a>
                        <a href="https://huggingface.co/antonisbast" target="_blank" 
                           style="margin: 0 1rem; text-decoration: none; font-size: 1.1rem;">
                            🌐 Hugging Face
                        </a>
                    </div>
                """)
                
                gr.Markdown("""
                ### Technical Details
                - **Powered by:** OpenAI GPT-4o-mini
                - **Framework:** Gradio
                - **Data Sources:** LinkedIn Profile, CV/Resume
                - **Features:** Function calling for contact recording and unanswered questions
                """)
        
        # Footer
        gr.HTML("""
            <footer>
                <p>🤖 Powered by ChatGPT & Gradio | Last Updated: 2025</p>
            </footer>
        """)
        
        def respond(message, history):
            """Handle chat response"""
            if not message.strip():
                return history, ""
            
            history.append({"role": "user", "content": message})
            yield history, ""  # First yield - shows user message right away
            bot_message = me.chat(message, history[:-1])
            history.append({"role": "assistant", "content": bot_message})
            yield history, ""  # Second yield - shows bot response
        
        def load_welcome():
            return [{"role": "assistant", "content": "Hello! I'm Antonis's AI assistant. I can answer questions about his experience in naval architecture, marine engineering, and AI/ML projects. What would you like to know?"}]
        
        # Chat events
        msg.submit(respond, [msg, chatbot], [chatbot, msg])
        submit_btn.click(respond, [msg, chatbot], [chatbot, msg])
        clear.click(lambda: [], None, chatbot, queue=False)
        
        
        # Load welcome message
        demo.load(load_welcome, None, chatbot)
    
    demo.launch(share=False)
    
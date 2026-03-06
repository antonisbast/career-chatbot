<<<<<<< HEAD
# 🤖 AI Career Chatbot - Antonis Bastoulis

An AI-powered chatbot that represents my professional profile and answers questions about my career, skills, and experience.

## 🌐 Try It Live

**➡️ [Chat with my AI assistant](https://huggingface.co/spaces/antonisbast/career-chatbot) ⬅️**

## 💡 What It Does

This chatbot acts as my professional representative, trained on my LinkedIn profile and CV. It can answer questions about:

- 💼 Work experience and career history
- 🛠️ Technical skills and expertise in Naval Architecture, Marine Engineering, and AI/ML
- 📁 Projects and achievements
- 🎓 Education and certifications
- 🎯 Professional interests and goals

### Smart Features

- **Professional Boundaries**: Automatically redirects inappropriate questions (personal life, salary, etc.)
- **Contact Collection**: Records visitor contact details directly to Google Sheets
- **Question Tracking**: Logs questions it couldn't answer for continuous improvement
- **Natural Conversation**: Speaks in first person while being transparent about being an AI

## 🛠️ Built With

- **AI Model**: OpenAI GPT-4o-mini
- **UI Framework**: Gradio
- **PDF Processing**: PyPDF (LinkedIn profile + CV)
- **Data Storage**: Google Sheets API
- **Deployment**: Hugging Face Spaces

## 📋 How It Works

1. Extracts information from PDF exports of my LinkedIn profile and CV
2. Uses GPT-4o-mini with a custom system prompt to represent me professionally
3. Employs function calling to record contacts and unanswered questions
4. Maintains professional boundaries while being helpful and informative

## 🔒 Privacy & Security

- No conversation history is permanently stored
- Contact information only used for professional follow-up
- Clear boundaries on what information is shared
- Secure API communication

---

## 👨‍💻 For Developers

Want to create your own AI career chatbot? Here's what you need:

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/antonisbast/career-chatbot.git
cd career-chatbot
```

2. **Install dependencies**
```bash
pip install openai gradio pypdf python-dotenv gspread oauth2client
```

3. **Prepare your documents**
- Export your LinkedIn profile as PDF
- Have your CV ready as PDF
- Create a brief summary text file

4. **Set up APIs**
- Get an OpenAI API key
- Set up Google Sheets API (for contact recording)
- Configure environment variables

5. **Run locally**
```bash
python app.py
```

### Key Files
- `app.py` - Main application with Gradio UI
- `me/linkedin.pdf` - LinkedIn profile export
- `me/CV.pdf` - Resume/CV
- `me/summary.txt` - Professional summary

### Customization
The system prompt in the `Me` class controls the chatbot's behavior, boundaries, and personality. Modify it to fit your professional profile.

---

## 📫 Connect With Me

- 🔗 [LinkedIn](https://www.linkedin.com/in/antonisbast/)
- 💻 [GitHub](https://github.com/antonisbast)
- 📧 [Email](mailto:antonisbast@gmail.com)
- 🌐 [Hugging Face](https://huggingface.co/antonisbast)

---

**⭐ If you found this project interesting, consider giving it a star!**

*Last Updated: November 2025*
=======
---
title: AI Career Chatbot - Antonis Bastoulis
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
---

# 🤖 AI Career Assistant - Antonis Bastoulis

Hi! I'm an AI assistant trained on Antonis's professional profile. Chat with me to learn about his experience in **Naval Architecture, Marine Engineering, and AI/ML**.

## 💬 What You Can Ask Me

- Work experience and projects
- Technical skills (Python, AI/ML, Naval Architecture)
- Education and certifications
- Career interests and goals

## 🔗 Want to Connect?

Just tell me your email in the chat and I'll make sure Antonis gets in touch with you!

## 🛠️ About This Bot

- Powered by **OpenAI GPT-4o-mini**
- Trained on LinkedIn profile + CV
- Maintains professional boundaries
- Records contacts via Google Sheets

---

**Connect with Antonis:**
[LinkedIn](https://www.linkedin.com/in/antonisbast/) • [GitHub](https://github.com/antonisbast) • [Email](mailto:antonisbast@gmail.com)
>>>>>>> huggingface/main

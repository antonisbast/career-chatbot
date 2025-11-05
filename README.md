# 🤖 Professional Career Chatbot

An AI-powered chatbot that represents your professional skills, experience, and career. Built with OpenAI's GPT API and Gradio.

## 🌟 Features

- **Interactive Chat**: Ask questions about professional background, skills, and experience
- **Unanswered Questions Tracking**: Automatically logs questions the bot couldn't answer
- **Contact Form**: Allows interested parties to leave their contact information
- **Professional Context**: Powered by CV and LinkedIn profile information

## 🚀 Live Demo

[Add your Hugging Face Spaces link here after deployment]

## 🛠️ Setup

### Prerequisites

- Python 3.9 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/career-chatbot.git
cd career-chatbot
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your_actual_api_key_here
```

6. Update the professional context in `app.py`:
   - Open `app.py`
   - Find the `load_professional_context()` function
   - Replace the placeholder text with your actual CV and LinkedIn content

### Running Locally

```bash
python app.py
```

The app will be available at `http://localhost:7860`

## 📦 Deployment

### Deploying to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Choose "Gradio" as the SDK
3. Clone your Space repository and add your code
4. Add your `OPENAI_API_KEY` in Space Settings > Variables and secrets
5. Push your code:
```bash
git add .
git commit -m "Initial commit"
git push
```

### Deploying to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/career-chatbot.git
git push -u origin main
```

**Important**: Never commit your `.env` file or any files containing API keys!

## 📊 Data Files

The application creates two JSON files to track:
- `unanswered_questions.json`: Questions the bot couldn't answer
- `contact_requests.json`: Contact information from interested users

## 🔒 Security

- API keys are stored in environment variables
- Sensitive files are excluded via `.gitignore`
- For production deployment, use Hugging Face Spaces secrets management

## 🤝 Contributing

This is a personal project, but feel free to fork and adapt it for your own use!

## 📝 License

MIT License - feel free to use this for your own professional chatbot!

## 👤 Author

[Your Name]
- LinkedIn: [Your LinkedIn Profile]
- Email: [Your Email]
- Portfolio: [Your Website]

---

*Built with ❤️ using OpenAI GPT and Gradio*

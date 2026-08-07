# 🤖 LYRA – AI Interview Coach

LYRA – AI Interview Coach is a full-stack AI-powered web application that helps students and job seekers prepare for technical interviews through interactive mock interview sessions. The platform generates AI-powered interview questions, evaluates user responses, provides detailed feedback, and generates interview reports.

---

## 🚀 Features

- 🔐 User Registration & Login
- 👤 User Profile Management
- 🤖 AI-Powered Interview Sessions
- 💬 Dynamic Interview Questions using Google Gemini API
- 📊 AI Answer Evaluation & Feedback
- 📄 PDF Interview Report Generation
- 📈 Interview Result Analysis
- 💾 MySQL Database Integration
- 📱 Responsive User Interface

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### Database
- MySQL

### AI Integration
- Google Gemini API

### Tools
- Git
- GitHub
- VS Code

---

## 📂 Project Structure

```
LYRA-AI-Interview-Coach/
│
├── app.py
├── backend/
│   ├── auth.py
│   ├── routes.py
│   ├── database.py
│   ├── interview.py
│   ├── report.py
│   ├── pdf_export.py
│   └── ai/
│       ├── ai_service.py
│       ├── prompts.py
│       ├── question_generator.py
│       ├── answer_evaluator.py
│       └── interview_manager.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── uploads/
│
├── reports/
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/Altaftamboli/LYRA-AI-Interview-Coach.git
```

### Move into Project

```bash
cd LYRA-AI-Interview-Coach
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Run Application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 🎯 Future Enhancements

- 🎙 Voice-based AI Interview
- 📹 Live Interview Session
- 🧠 Resume-based Question Generation
- 📊 Performance Analytics Dashboard
- ☁ Cloud Deployment
- 📧 Email Authentication
- 🏆 Interview History Tracking

---

## 👨‍💻 Contributors

### Manoj 
- Frontend Development
- Responsive UI Design
- Landing Page Development
- Interview Dashboard
- Login & Authentication UI
- Interview History Interface

### Altaf Tamboli
- Backend Development
- Flask Integration
- MySQL Database
- Authentication
- Frontend–Backend Integration
- AI Module Integration

### Rohan
- AI module development
- LLM integration (Gemini/Groq)
- Prompt engineering
- AI answer evaluation and scoring
- AI report generation
- AI Module testing and debugging
- API Key Management

---

## 📜 License

This project is developed for educational and portfolio purposes.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

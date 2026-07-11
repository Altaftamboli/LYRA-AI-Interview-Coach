# AI Interview Coach

## Overview

AI Interview Coach is a web-based application that helps users prepare for technical interviews. It provides user authentication, an interview dashboard, AI-based interview pages, result analysis, and report generation using a Flask backend with a responsive frontend.

---

## Features

- User Registration
- User Login
- Dashboard
- AI Interview Page
- Interview Result Page
- PDF Report Export
- Responsive UI
- Flask Backend
- MySQL Database Integration

---

## Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python
- Flask
- MySQL
- Werkzeug

---

## Project Structure

```
Group-project/
│
├── backend/
│   ├── auth.py
│   ├── database.py
│   ├── interview.py
│   ├── pdf_export.py
│   ├── report.py
│   ├── routes.py
│   └── config.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── interview.html
│   └── result.html
│
├── static/
│   ├── style.css
│   ├── responsive.css
│   └── js/
│       ├── login.js
│       ├── register.js
│       ├── dashboard.js
│       ├── interview.js
│       └── result.js
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Altaftamboli/Group-project.git
```

### Open Project

```bash
cd Group-project
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Create a MySQL database and update the connection details in:

```
backend/config.py
```

---

## Run Application

```bash
python app.py
```

Open in your browser:

```
http://127.0.0.1:5000
```

---

## Application Flow

```
Home
   ↓
Register
   ↓
Login
   ↓
Dashboard
   ↓
Start Interview
   ↓
Interview
   ↓
Result
   ↓
PDF Report
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/register | Register User |
| POST | /api/login | User Login |

---

## Contributors

- Altaf Tamboli (Project Owner)
- Rohan ingale (AI integration)
- Manoj Khandare (Frontend Developer)

---

## Future Improvements

- AI Question Generation
- JWT Authentication
- Email Verification
- Profile Management
- Interview History
- Performance Analytics

---

## License

This project is developed for educational purposes.

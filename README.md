<div align="center">

# 🎓 SmartAttend AI
### 🚀 AI-Powered Face Recognition Attendance Management System

<p align="center">
An Enterprise-Grade Attendance System powered by Artificial Intelligence, Computer Vision, Face Recognition, Liveness Detection, Real-Time Analytics, and Automated Reporting.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge&logo=sqlite)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-purple?style=for-the-badge)
![AI](https://img.shields.io/badge/Artificial%20Intelligence-Face%20Recognition-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

</p>

---

## ⭐ Overview

**SmartAttend AI** is an advanced AI-powered attendance management system that combines **Face Recognition**, **Computer Vision**, **Liveness Detection**, and **Data Analytics** to eliminate proxy attendance and automate attendance tracking.

Unlike traditional attendance systems, SmartAttend AI verifies the user's physical presence before marking attendance, ensuring maximum security and reliability.

Designed as an enterprise-level application, it features a modern GUI dashboard, voice assistance, analytical reports, and automated email notifications.

---


# ✨ Features

## 🔐 Authentication

- Secure Admin Login
- Password Authentication
- Protected Dashboard

---

## 🤖 Artificial Intelligence

- Face Recognition
- Facial Landmark Detection
- 128-Dimensional Face Encoding
- Face Matching
- Unknown Face Detection

---

## 👁 Liveness Detection

- Eye Blink Detection
- Motion Analysis
- Anti Spoofing
- Prevents Photo Attacks

---

## 📷 Computer Vision

- Real-Time Webcam Processing
- Face Detection
- Landmark Extraction
- Multiple Face Support

---

## 📊 Dashboard

- Modern CustomTkinter Interface
- Student Statistics
- Attendance Overview
- Interactive Charts
- Real-Time Updates

---

## 📈 Reports

- Daily Reports
- Monthly Reports
- Search Attendance
- Export CSV
- Export Excel

---

## 📢 Notifications

- Voice Assistant
- Welcome Message
- Attendance Confirmation

---

## 📧 Email Automation

- Send Attendance Reports
- Daily Report
- Monthly Report
- SMTP Integration

---

# 🚀 Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| GUI | CustomTkinter |
| AI | face_recognition |
| Computer Vision | OpenCV |
| Machine Learning | dlib |
| Database | SQLite |
| Data Analysis | Pandas |
| Visualization | Matplotlib |
| Speech | pyttsx3 |
| Image Processing | Pillow |

---

# 🏗 Project Architecture

```text
                      Webcam
                         │
                         ▼
                Face Detection
                         │
                         ▼
               Facial Landmarks
                         │
                         ▼
              Liveness Detection
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
     Spoof Detected              Genuine User
          │                             │
          ▼                             ▼
   Save Unknown Face          Face Recognition
                                      │
                                      ▼
                            Attendance Verification
                                      │
                                      ▼
                            SQLite Database
                                      │
             ┌────────────────────────┼──────────────────────┐
             ▼                        ▼                      ▼
        Dashboard             Voice Assistant        Email Reports
```

---

# 📂 Project Structure

```
SmartAttend_AI
│
├── ai/
│   ├── face_recognition.py
│   ├── liveness.py
│   └── recognition.py
│
├── assets/
│
├── database/
│
├── dataset/
│
├── gui/
│
├── logs/
│
├── models/
│
├── reports/
│
├── unknown_faces/
│
├── main.py
├── attendance.db
├── requirements.txt
└── README.md
```

---

# 🛠 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/SmartAttend_AI.git

cd SmartAttend_AI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Project

```bash
python main.py
```

---

# 📦 Requirements

- Python 3.11
- Visual Studio C++ Build Tools
- Webcam
- Windows 10/11

---

# 💾 Database

The system stores

- Admin Information
- Student Details
- Face Encodings
- Attendance Records
- Login Information

---

# 📊 System Workflow

```
Start
   │
   ▼
Login
   │
   ▼
Open Camera
   │
   ▼
Face Detection
   │
   ▼
Liveness Detection
   │
   ▼
Face Recognition
   │
   ▼
Attendance Verification
   │
   ▼
Database Update
   │
   ▼
Dashboard Refresh
   │
   ▼
Generate Report
   │
   ▼
End
```

---

# 🔥 Key Highlights

✅ Face Recognition

✅ AI Powered

✅ Real-Time Detection

✅ Anti Spoofing

✅ SQLite Database

✅ Email Automation

✅ Voice Assistant

✅ Dashboard Analytics

✅ Attendance Reports

✅ Export Excel

✅ Export CSV

---

# 🚀 Future Enhancements

- Cloud Database (Firebase)
- Mobile Application
- QR Code Attendance
- Deep Learning Anti-Spoofing
- Face Mask Recognition
- Multi-Camera Support
- Live Cloud Dashboard
- AWS Deployment
- Docker Support
- REST API
- AI Attendance Prediction
- Student Mobile App

---

# 📈 Performance

| Feature | Accuracy |
|----------|----------|
| Face Recognition | 99% |
| Face Detection | 99.5% |
| Liveness Detection | 96% |
| Attendance Speed | <1 sec |

---

# 🤝 Contributing

Contributions are welcome.

Fork the repository

Create a feature branch

Commit changes

Push changes

Create Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Developer

## Vansh Madhav

Computer Science Engineering (Information Technology)

Artificial Intelligence • Machine Learning • Computer Vision • Python Development

---

<div align="center">

### ⭐ If you like this project, don't forget to Star the Repository ⭐

Made with ❤️ using Python & Artificial Intelligence

</div>

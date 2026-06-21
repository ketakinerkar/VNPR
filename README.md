# Vehicle Number Plate Recognition (VNPR)

## Overview

Vehicle Number Plate Recognition (VNPR) is an AI-powered vehicle identification and access management system that detects vehicle number plates using YOLO, extracts plate text using Google Vision OCR, verifies vehicles against a registered database, maintains entry/exit logs, and sends email notifications to vehicle owners.

The system is designed for use in residential societies, educational institutions, corporate campuses, parking facilities, and other secure access-control environments.

---

## Key Features

### Vehicle Registration

* Register vehicle owner information.
* Store vehicle details in the database.
* Upload and save vehicle images.
* Store chassis number and vehicle number.
* Maintain a centralized registered vehicle database.

### Number Plate Detection

* Capture vehicle images using a camera.
* Detect number plates using YOLO.
* Automatically crop the detected plate region.
* Process images through OCR for text extraction.

### OCR-Based Recognition

* Extract number plate text using Google Vision API.
* Clean and format recognized text.
* Handle noisy and partially detected plates.

### Fuzzy Matching

* Compare OCR output with registered vehicle records.
* Correct OCR mistakes using fuzzy string matching.
* Improve recognition accuracy.

### Vehicle Verification

* Verify whether the detected vehicle exists in the database.
* Display owner information for authorized vehicles.
* Identify unauthorized or unknown vehicles.

### Entry/Exit Management

* Automatically create entry logs.
* Automatically update exit logs.
* Maintain complete vehicle movement history.

### Email Notifications

* Send entry notifications to vehicle owners.
* Send exit notifications to vehicle owners.
* Provide timestamp information for every vehicle movement.

### Vehicle Logs

* Store all vehicle movement records.
* View entry and exit timestamps.
* Track vehicle activity history.

---

## Tech Stack

| Component            | Technology              |
| -------------------- | ----------------------- |
| Frontend             | Streamlit               |
| Backend              | FastAPI                 |
| Database             | SQLite                  |
| Object Detection     | YOLO                    |
| OCR                  | Google Cloud Vision API |
| Image Processing     | OpenCV                  |
| Matching             | FuzzyWuzzy              |
| Programming Language | Python                  |

---

## System Workflow

```text
Vehicle Image Capture
          ↓
YOLO Number Plate Detection
          ↓
Plate Region Extraction
          ↓
Google Vision OCR
          ↓
Text Cleaning & Formatting
          ↓
Fuzzy Matching
          ↓
Database Verification
          ↓
Entry/Exit Logging
          ↓
Email Notification
          ↓
Display Vehicle Information
```

---


## Screenshots

* Login Page

<img width="1920" height="858" alt="image" src="https://github.com/user-attachments/assets/b22bf12f-cd65-4171-ba3c-c1226cdadbe9" />
<img width="1920" height="865" alt="image" src="https://github.com/user-attachments/assets/1c5e4b0c-3177-42ec-912c-35caf9da9873" />


* Dashboard
  <img width="1919" height="834" alt="image" src="https://github.com/user-attachments/assets/5d1943ff-69b1-475f-ba11-c3f28b2cef6d" />

* Vehicle Registration
  <img width="1918" height="844" alt="image" src="https://github.com/user-attachments/assets/708d2d17-e5de-429c-880e-593a7a75b089" />

* Number Plate Recognition
  (Screen Recording)
https://github.com/user-attachments/assets/ed1d3ad1-37f5-4166-b10d-a7292eddd45c


* Vehicle Logs
  <img width="1919" height="857" alt="image" src="https://github.com/user-attachments/assets/6bb2310c-38fd-4438-9630-39bb8e3d59e3" />

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd VNPR
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_APPLICATION_CREDENTIALS=credentials/vision.json

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Run FastAPI Backend

```bash
uvicorn app.api.main:app --reload
```

### Run Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

---

## Future Enhancements

* Real-time video stream processing.
* Fully automated vehicle detection.
* Multiple camera support.
* Cloud database integration.
* Vehicle blacklist and whitelist management.
* Admin analytics dashboard.
* SMS notification support.
* Cloud deployment.

---


## Learning Outcomes

* Computer Vision with YOLO
* Optical Character Recognition (OCR)
* FastAPI REST API Development
* Streamlit Application Development
* Database Management with SQLite
* Image Processing using OpenCV
* Email Automation
* AI-powered Vehicle Access Control Systems

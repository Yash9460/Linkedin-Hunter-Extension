# 🔍 LinkedIn Hunter Extension

A **Chrome Extension + FastAPI Backend** that fetches LinkedIn profile details:  
**Full Name, Email, Organisation, Designation**.  
Emails are enriched via the [Hunter.io](https://hunter.io) API.

---

## 📊 Badges

![Made with FastAPI](https://img.shields.io/badge/Made%20with-fastapi-blue?logo=fastapi)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-orange?logo=google-chrome)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/Yash9460/Linkedin-Hunter-Extension.git
cd Linkedin-Hunter-Extension
```

### 2. Setup Flask Backend

```bash
cd python-backend
pip install -r requirements.txt
```

## Edit app.py and replace:

API_KEY = "PUT_YOUR_HUNTER_API_KEY_HERE"

## Run backend:
```bash
uvicorn app:app --reload --port 5000
```

#### Backend runs at: http://127.0.0.1:5000

### 3. Load Chrome Extension

- Open Chrome → Extensions → Manage Extensions
- Enable Developer Mode (top-right toggle)
- Click Load Unpacked → Select the linkedin-hunter-extension/ folder

## 🧪 Testing

1. Open LinkedIn profile (e.g.):
   [Raman Ghai](https://www.linkedin.com/in/raman-ghai-8bb7b418/)

2. Click the extension icon.

3. You should see:

- ✅ Name
- ✅ Organisation
- ✅ Designation
- ✅ Email (from Hunter.io)

##### 👉 If no email is found → “Not found” is shown.

### ⚡ Notes

- Chrome Extension scrapes Name, Designation, Organisation directly from LinkedIn DOM.
- Flask Backend calls Hunter.io API to fetch the most probable email.
- Email fetching depends on Hunter.io free quota (50 requests/month).

# Shorty — A Django URL Shortener API

An URL shortener built with **Django 5** and **Django REST Framework**.  
Supports short links, expiry, click limits, QR codes, and stats.  

---

## ✨ Features
- 🔗 Create short links with custom or auto-generated alias  
- ⏳ Optional expiry date and max-clicks limit  
- 📉 Click counting with live stats  
- 🚫 Expired/disabled/maxed links return JSON errors  
- 📊 Stats endpoint for each link  
- 🖼️ Preview endpoint for link metadata  
- 📱 QR code endpoint for quick sharing  
- 🛡️ Rate limiting (100 new links/hour per IP)  
- ✅ Browsable API (thanks DRF)

---

## 🚀 Quickstart

### 1. Clone & install dependencies
```bash
git clone https://github.com/coganka/django-url-shortener.git
cd shorty
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start server
```bash
python manage.py runserver
```

Now available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠 API Endpoints

### ➕ Create a short link
```http
POST /api/links/
Content-Type: application/json
```

Body:
```json
{
  "original_url": "https://google.com",
  "max_clicks": 5
}
```

Response:
```json
{
  "id": 1,
  "original_url": "https://google.com",
  "alias": "Ab3xYz",
  "short_url": "http://127.0.0.1:8000/Ab3xYz/",
  "qr_url": "http://127.0.0.1:8000/q/Ab3xYz.png",
  "created_at": "2025-08-31T12:34:56Z",
  "expires_at": null,
  "clicks_count": 0,
  "max_clicks": 5,
  "active": true,
  "is_expired": false
}
```

---

### 📋 List all links
```http
GET /api/links/
```

---

### 🔍 Get link detail
```http
GET /api/links/<id>/
```

---

### 🗑️ Delete link
```http
DELETE /api/links/<id>/
```
- If **soft delete enabled** → marks inactive.  
- If **hard delete** → removes row completely.  

---

### 📊 Link stats
```http
GET /api/links/<id>/stats/
```

Response:
```json
{
  "id": 1,
  "alias": "Ab3xYz",
  "original_url": "https://google.com",
  "short_url": "http://127.0.0.1:8000/Ab3xYz/",
  "qr_url": "http://127.0.0.1:8000/q/Ab3xYz.png",
  "clicks_count": 2,
  "expires_at": null,
  "is_expired": false,
  "active": true,
  "created_at": "2025-08-31T12:34:56Z",
  "max_clicks": 5
}
```

---

### ↪️ Redirect
Open in browser:
```
http://127.0.0.1:8000/Ab3xYz/
```
- Redirects to original URL  
- Increments click count  

Error examples:
```json
{"detail": "Link expired"}
{"detail": "Click limit reached"}
{"detail": "Link disabled"}
```

---

### 🖼️ Preview
```http
GET /p/<alias>/
```
Returns link info without redirect.

---

### 📱 QR Code
```
GET /q/<alias>.png
```
Returns a PNG QR code pointing to the short link.

---

## ⏳ Rate Limiting
- Link creation (`POST /api/links/`) is limited to **100 requests/hour per IP**.  
- If exceeded:
```json
{"detail": "Request was throttled. Expected available in X seconds."}
```

---


## 📌 Tech Stack
- Python 3.11+
- Django 5
- Django REST Framework
- qrcode + pillow (for QR codes)

---

# 🥗 Calorie Tracker

A full-stack **Django-based Calorie & Macro Tracker** web application that helps users monitor their daily nutrition, track meals, and visualize macro intake.

Built as a portfolio project with a focus on **clean architecture, real-world features, and production-ready practices**.

---

## 🚀 Features

- 🔐 User Authentication (Login / Signup / Logout)
- 📊 Track daily calories & macros (Protein, Carbs, Fats)
- 🍽️ Add, update, and delete food entries
- 📅 Daily food log system
- 📈 Macro visualization using charts
- ⚡ Dynamic UI updates with HTMX (no heavy JS frameworks)
- 🎨 Clean UI with Tailwind CSS
- 🧠 Backend-driven calculations (no frontend hacks)

---

## 🛠️ Tech Stack

### Backend
- Django (CBVs preferred)
- Django ORM
- Django Allauth (Authentication)

### Frontend
- Django Templates
- Tailwind CSS

### Interactivity
- HTMX (AJAX without JS complexity)

### Visualization
- Chart.js (Macro tracking graphs)

---

## 📂 Project Structure


calorie-tracker/
│
├── tracker/ # Core app (models, views, logic)
├── users/ # Authentication & user profiles
├── templates/ # HTML templates
├── static/ # CSS, JS, assets
├── manage.py
└── requirements.txt


---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Inder0/Calorie-tracker.git
cd Calorie-tracker
2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Setup environment variables
Create a .env file:
SECRET_KEY=your_secret_key
DEBUG=True
5️⃣ Run migrations
python manage.py migrate
6️⃣ Create superuser
python manage.py createsuperuser
7️⃣ Run server
python manage.py runserver

📊 How It Works
Users log their meals with calorie + macro data
Data is stored in the database (no frontend-only calculations)
Daily totals are computed dynamically
Charts visualize macro distribution

This follows the standard calorie tracking workflow seen in modern apps

🧩 Future Improvements

📊 Weekly & monthly analytics
🧠 AI-based meal suggestions
📦 API integration (USDA / OpenFoodFacts)

🧪 Learning Outcomes

Full-stack Django development
Working with relational databases
Authentication flows (Allauth)
Using HTMX for dynamic UI
Structuring production-ready apps

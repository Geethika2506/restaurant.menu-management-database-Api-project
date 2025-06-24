# restaurant.menu-management-database-Api-project

# 🍽️ Restaurant Menu Management System

A full-stack web application for managing a restaurant's menu, built with:
- 🐍 Django REST Framework (Backend)
- 🍃 MongoDB (Database)
- ⚛️ React + Tailwind CSS (Frontend via Vite)

---

## 📂 Project Structure

Restaurant_Menu_DB-1/
│
├── Restaurant_Menu_DB/
│ ├── restaurant_app/ # Django app with models, views, serializers, etc.
│ └── restaurant_project/ # Django project config
│
├── manage.py # Django project manager
├── requirements.txt # Python dependencies
│
├── restaurant-menu-frontend/ # Frontend built with React + Tailwind + Vite
│ ├── public/
│ ├── src/
│ ├── index.html
│ ├── vite.config.js
│ └── tailwind.config.js



---

## ⚙️ Features

- CRUD operations for menu items
- REST API integration
- MongoDB as the database backend
- Clean, responsive UI using Tailwind CSS
- Separate frontend and backend architecture

---

## 🔧 Tech Stack

### Backend:
- Django
- Django REST Framework
- Djongo / pymongo (MongoDB connector)

### Frontend:
- React
- Tailwind CSS
- Vite (fast dev server and bundler)

---

## 🚀 Getting Started

### Backend Setup (Django + MongoDB)

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/restaurant-menu-db.git
cd Restaurant_Menu_DB-1
#create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

#Install dependencies
pip install -r requirements.txt

#Configure MongoDB in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'restaurant_db',
    }
}

#Run migrations & start server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

#Frontend Setup (React + Vite)



```bash
1.Navigate to frontend folder
cd restaurant-menu-frontend

2.Install Node dependencies
npm install

3.Run development server
npm run dev
```
Access the frontend at: http://localhost:5173

📡 API Endpoints
Method	Endpoint	Description
GET	/api/menu/	List all menu items
POST	/api/menu/	Create a new menu item
GET	/api/menu/:id/	Retrieve a single item
PUT	/api/menu/:id/	Update a menu item
DELETE	/api/menu/:id/	Delete a menu item

#To-Do (Enhancements)
Authentication (Login/Signup)

Role-based access (Admin/Staff)

Search and filter menu items

Deployment (Docker + Render/Vercel)




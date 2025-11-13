# 💰 Expense Tracker — Django Project

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Django](https://img.shields.io/badge/Django-5.x-green.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📘 Overview
The **Expense Tracker** is a web-based application developed using **Django** that helps users manage their **daily income and expenses** in an organized and efficient way.  
It enables users to record, analyze, and visualize their financial data with a clean and user-friendly interface.

This project demonstrates full-stack development skills including:
- Backend development with Django  
- Database integration with MySQL  
- Authentication and user management  
- Frontend templating with HTML, CSS, and JavaScript  

---

## 🚀 Features

### 👥 User Management
- Secure user **Registration, Login, and Logout**
- Individual dashboards for each user
- Password hashing and session-based authentication

### 💸 Income & Expense Tracking
- Add, edit, and delete income or expense entries  
- Categorize transactions (e.g., Food, Bills, Travel, Salary)  
- View recent transactions with timestamps  

### 📊 Dashboard & Analytics
- Visual summary of total **income, expenses, and balance**  
- Filter transactions by **date, type, or category**  
- Generate insights into spending habits  

### ⚙️ Admin Panel
- Full control through Django’s built-in **Admin Interface**
- Admins can manage users and all financial records  

### 🗄️ Database
- Data stored securely using **MySQL**  
- Environment-based configuration for local or production setups  

---

## 🏗️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Backend Framework** | Django (Python) |
| **Database** | MySQL |
| **Frontend** | HTML, CSS, JavaScript |
| **Authentication** | Django Auth System |
| **Version Control** | Git & GitHub |
| **Deployment** | Localhost / Cloud (optional) |

---

## 🪜 Installation & Setup

### 🔧 Prerequisites
Make sure you have the following installed:
- Python 3.x  
- MySQL Server  
- Git  
- Virtual Environment (recommended)

### ⚙️ Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Dudekularajesh/Expense_Tracker_App.git
   
   cd Expense_Tracker_App
   
Create Virtual Environment


python -m venv myenv

Activate Virtual Environment


myenv\Scripts\activate       # On Windows

source myenv/bin/activate    # On Mac/Linux

Install Dependencies


pip install -r requirements.txt

Configure MySQL Database

Edit the DATABASES section in expense_tracker/settings.py:


DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.mysql',
        
        'NAME': 'expense_tracker',
        
        'USER': 'root',
        
        'PASSWORD': 'your_password',
        
        'HOST': '127.0.0.1',
        
        'PORT': '3306',
        
    }
    
}

Run Migrations


python manage.py makemigrations

python manage.py migrate

Create Superuser


python manage.py createsuperuser

Start the Development Server


python manage.py runserver

Access the App

User Site → http://127.0.0.1:8000/

Admin Site → http://127.0.0.1:8000/admin/


📁 Project Structure

Expense_Tracker_App/

│
├── expense_tracker/         # Main Django project

│   ├── settings.py          # Project settings

│   ├── urls.py              # Global URLs

│   └── wsgi.py              # WSGI entry point
│

├── tracker/                 # Core app

│   ├── models.py            # Database models

│   ├── views.py             # View logic

│   ├── urls.py              # App routes

│   ├── templates/           # HTML templates

│   ├── static/              # CSS, JS, Images

│   └── forms.py             # Input forms
│
├── manage.py                # Django management script

└── requirements.txt         # Python dependencies


📈 Future Enhancements

💳 Add budget limits and savings goals

📅 Monthly PDF/Excel report generation

📊 Add chart visualizations using Chart.js or Plotly

📱 Responsive mobile-friendly interface

🌐 Deployed on (Render)


👨‍💻 Author

Dudekula Rajesh

Full Stack Developer | Python & Django Enthusiast

📧 Email: dudekularajesh3337@gmail.com

💻 GitHub: https://github.com/Dudekularajesh

🌐 Portfolio: https://dudekularajeshportfolio.netlify.app/

🌐 Project Live: https://expense-tracker-7voh.onrender.com


📝 License

This project is licensed under the MIT License.
See the LICENSE file for details.


⭐ Acknowledgements

Special thanks to:

Django Community Documentation

MySQL Developers

Open Source Contributors

If you like this project, ⭐ Star this repository and share your feedback!

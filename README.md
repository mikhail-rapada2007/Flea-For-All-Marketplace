# Flea-For-All-Marketplace
A peer-to-peer marketplace web application built with Django, inspired by platforms like Facebook Marketplace. Developed for Object-Oriented Programming (CPE 201), Holy Angel University, Group 2, SY 2026-2027.
This is the official output of Group 2 of CPE-201, 2026-2027. 

Live Website Link: https://fleaforall.pythonanywhere.com/

## Tech Stack
- **Backend:** Python 3.9.13, Django 4.2.30
- **Frontend:** HTML 5, Bootstrap 5
- **Database:** SQLite (local development)

## Getting Started

Follow these steps to set up the project on your own machine.

### 1. Clone the repository
-> git clone https://github.com/mikhail-rapada2007/Flea-For-All-Marketplace.git

-> cd Flea-For-All-Marketplace/flea_for_all


### 2. Create and activate a virtual environment
-> python -m venv venv


Windows (PowerShell):
venv\Scripts\Activate.ps1


Windows (Command Prompt):
venv\Scripts\activate.bat


Mac/Linux:
source venv/bin/activate


### 3. Install dependencies

python -m pip install -r requirements.txt

> Note: always use `python -m pip` rather than a bare `pip` command — on some systems, `pip` alone can silently point to a different Python installation than the one your venv actually uses.


### 4. Set up environment variables

Duplicate the `.env.example` and rename it as a new file named `.env` in the project root.

Open `.env` and fill in the values:

`EMAIL_HOST_USER = email_here`

`EMAIL_HOST_PASSWORD = password_here`

`SECRET_KEY = secret_key_here`

`DEBUG = True`

`ALLOWED_HOSTS = 127.0.0.1, localhost`

To generate a SECRET_KEY, run:
`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

To obtain the host email and password, please email the members of the group.


### 5. Apply database migrations

python manage.py migrate


### 6. Create a superuser (for admin panel access)

python manage.py createsuperuser


### 7. Run the development server

python manage.py runserver


Visit `http://127.0.0.1:8000/` in your browser. Admin panel is available at `http://127.0.0.1:8000/admin/`.

## Features

### Accounts
- User signup, login, and logout (Django's built-in authentication)
- Email Verification is implemented
- Every new account automatically gets a linked Store/Profile

### Marketplace
- Product listings with title, description, price, condition, and category
- Category-based filtering
- Search Bar system
- Product status control (Available / Reserved / Sold), visible as color-coded badges site-wide
- Detailed item view for each product

### Stores
- Individual store pages for every user, showing their active listings
- Every user can change the layout of their store
- Uploadable Pictures for the profile picture, store banner, and items to be sold. 
- Store FAQ (sellers can add their own frequently asked questions)
- Store reviews with separate buyer and seller ratings

### Messaging
- Persistent chat between buyers and sellers, accessible as a floating widget across the site
- Full conversation history and an inbox view

### Trust & Safety
- Report system for both individual products and entire stores, with a defined set of report reasons
- Reports reviewable through the admin dashboard

### Other
- Terms and Services page

## Known Limitations

- Uploaded images are stored locally only; cloud-based image storage is not implemented
- Chat is not realtime
- Rapidly clicking publish listing leads to duplicate listings

## Team

| Member | Role |
|---|---|
| Mikhail Rapada | Initial Models, Authentication, Email Verification, Detailed Item View, Report System, Admin Dashboard |
| Brix Palac | Store Listings, Store Profile View, Store FAQ, Chat Feature |
| Jemimah Salucop | Terms and Services, Store Review, Category Search, General Search |
| Prince Ubando | Product Listings, Store Customizability, Sell Item Function, CSS Design, Chat Feature |
| Andrew Bagaporo | Product Status Control, Report System, Bug Fixes |

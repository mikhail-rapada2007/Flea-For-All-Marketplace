# Flea-For-All-Marketplace
A peer-to-peer marketplace web application built with Django, inspired by platforms like Facebook Marketplace. Developed for Object-Oriented Programming (CPE 201), Holy Angel University, Group 2, SY 2026-2027.
This is the official output of Group 2 of CPE-201, 2026-2027. 

## Tech Stack
- **Backend:** Python, Django
- **Frontend:** HTML, Bootstrap 5
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


### 4. Apply database migrations

python manage.py migrate


### 5. Create a superuser (for admin panel access)

python manage.py createsuperuser


### 6. Run the development server

python manage.py runserver


Visit `http://127.0.0.1:8000/` in your browser. Admin panel is available at `http://127.0.0.1:8000/admin/`.

## Features

### Accounts
- User signup, login, and logout (Django's built-in authentication)
- Every new account automatically gets a linked Store/Profile

### Marketplace
- Product listings with title, description, price, condition, and category
- Category-based filtering
- Product status control (Available / Reserved / Sold), visible as color-coded badges site-wide
- Detailed item view for each product

### Stores
- Individual store pages for every user, showing their active listings
- Store FAQ (sellers can add their own frequently asked questions)
- Store reviews with separate buyer and seller ratings
- Verified store badge

### Messaging
- Persistent chat between buyers and sellers, accessible as a floating widget across the site
- Full conversation history and an inbox view

### Trust & Safety
- Report system for both individual products and entire stores, with a defined set of report reasons
- Reports reviewable through the Django admin panel

### Other
- Terms and Services page

## Known Limitations

- Uploaded images are stored locally only; cloud-based image storage is planned but not yet implemented
- Store layout customization is not yet available
- Email verification for login is not yet implemented

## Team

| Member | Role |
|---|---|
| Mikhail Rapada | Models, Authentication, Admin Panel, Detailed Item View, Report System |
| Brix Palac | Store Listings, Store Profile View, Store FAQ, Chat Feature |
| Jemimah Salucop | Terms and Services, Store Review, Category Search |
| Prince Ubando | Product Listings, Sell Item Function, CSS Design |
| Andrew Bagaporo | Product Status Control, Report System |

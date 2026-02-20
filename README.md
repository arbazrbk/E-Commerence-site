# ShoppingX E-Commerce Django Project

## Overview
ShoppingX is a full-featured e-commerce web application built with Django. It supports user registration, login, product browsing, cart management, order placement, and more. The project uses Django's authentication system and Bootstrap for a modern UI.

## Features
- User registration and login
- Profile management
- Product listing by category (mobile, laptop, topwear, bottomwear)
- Add to cart, remove from cart, and update cart quantity
- Checkout and order placement
- Payment success confirmation
- Address management
- Password change and reset

## Project Structure
```
shopingx/
│
├── rbk/                  # Main Django app
│   ├── templates/rbk/    # HTML templates
│   ├── static/rbk/       # Static files (CSS, JS, images)
│   ├── models.py         # Database models
│   ├── views.py          # View functions and classes
│   ├── forms.py          # Django forms
│   ├── urls.py           # App URL routes
│   └── ...
├── shopingx/             # Project settings and URLs
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
└── env/                  # Python virtual environment
```

## Setup Instructions
1. **Clone the repository**
2. **Create and activate a virtual environment**
3. **Install dependencies**
   ```
   pip install django pillow
   ```
4. **Apply migrations**
   ```
   python manage.py migrate
   ```
5. **Create a superuser (admin)**
   ```
   python manage.py createsuperuser
   ```
6. **Run the development server**
   ```
   python manage.py runserver
   ```
7. **Access the app**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
- Register a new user or log in with an existing account.
- Browse products, add them to your cart, and proceed to checkout.
- Place orders and view order history.
- Manage your profile and addresses.

## Notes
- Static files (CSS/JS/images) should be placed in `rbk/static/rbk/`.
- Templates are in `rbk/templates/rbk/`.
- For production, configure proper static/media file serving and security settings.

## License
This project is for educational purposes.

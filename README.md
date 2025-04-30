# EcomDjango Project

## Overview
EcomDjango is a Django-based e-commerce application that allows users to browse products, place orders, and manage their accounts. The application includes an admin dashboard for managing users and orders.

---

## Project Setup

### Prerequisites
- Python 3.10 or higher
- Django 5.2
- SQLite (default database)
- SQLite Browser

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ecom-django.git
   cd ecom-django

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Apply database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Run the development server:
    ```bash
    python manage.py runserver

6. Access the application at http://127.0.0.1:8000.

### Database Migration Script
```bash
To set up the database, run the following commands:
    python [manage.py](http://_vscodecontentref_/1) makemigrations
    python [manage.py](http://_vscodecontentref_/2) migrate
```

### Project Structure
```bash
csv_import_project/
│
├── csv_import_project/          # Project settings and configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Project-level URL configuration
│   └── wsgi.py                  # WSGI entry point
│
├── importer/                    # Main application
│   ├── management/
│   │   ├── commands/            # Folders for run commands
│   │       ├── importcsv.py     # Import data from csv to SQLite database
│   ├── migrations/              # Database migration files
│   ├── templates/               # HTML templates
│   │   ├── importer/            # App-specific templates
│   │       ├── product_list.html
│   │       ├── product_detail.html
│   │       ├── order_history.html
│   │       └── admin_dashboard.html
│   ├── static/                  # Static files (CSS, JS, images)
│   ├── models.py                # Database models
│   ├── views.py                 # Application views
│   ├── urls.py                  # App-level URL configuration
│   └── tests.py                 # Unit tests
│
└── [db.sqlite3](http://_vscodecontentref_/3)                   # SQLite database
```

### Models
```bash
1. User
    Fields: id, user_name, full_name, email, phone, user_type
    Purpose: Stores user information (admin or customer).
2. Product
    Fields: id, name, price, description, image_urls
    Purpose: Stores product details.
3. Order
    Fields: id, buyer_phone, product, quantity, order_date
    Purpose: Tracks orders placed by users.
```

### Views
```bash
1. Register
    URL: /register/
    Allows users to register an account.
2. Login
    URL: /login/
    Allows users to log in as a customer or admin.
3. Product List
    URL: /product_list/
    Displays all available products.
4. Product Detail
    URL: /product/<id>/
    Displays product details and allows users to place an order.
5. Order History
    URL: /order_history/
    Displays the order history for the logged-in user.
6. Admin Dashboard
    URL: /admin_dashboard/
    Displays user and order statistics for admins.
```

### Templates
```bash
1. product_list.html
    Displays a list of all products.
2. product_detail.html
    Displays product details and includes an order form.
3. order_history.html
    Displays the logged-in user's order history.
4. admin_dashboard.html
    Displays user and order statistics for admins.
```

### Functionalities
```bash
1. User Registration and Login
    Users can register and log in as customers or admins.
2. Product Browsing
    Users can view a list of products and their details.
3. Product Searching
    User can search product by name
4. Order Placement
    Users can place orders for products.
5. Order History
    Users can view their past orders.
6. Admin Dashboard
    Admins can view user and order statistics.
7. Error Handling
    Basic error handling for invalid input and unauthorized access.
8. Session Management
    User sessions are managed for authentication and authorization.
```

### Testing
```bash
The application includes unit tests for key functionalities:
    - User registration and login
    - Product listing and detail views
    - Order placement
    - Admin dashboard access
```

### Run the tests using:
    python manage.py test importer

### Open Source Data License:
Data (data.csv) has been downloaded from 
```bash
https://github.com/octaprice/ecommerce-product-dataset/blob/main/README.md
```
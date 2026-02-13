# Sales-system-API
A Django REST API for managing invoices, and payments. Built with Django, and deployed-ready for Azure.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL (comming soon)
- Azure (if deployed)


  ## Features

- User authentication (JWT)
- CRUD operations for products
- Invoice generation
- Filtering and search

  ## Database Models

- Sale
- SaleItem
- Product
- Store
- Inventory


## Installation

1. Clone the repository

git clone https://github.com/yourusername/project-name.git

2. Create virtual environment

python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Run migrations

python manage.py migrate

5. Run server

python manage.py runserver

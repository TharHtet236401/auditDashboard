# Transaction Audit Dashboard

## Overview
This project is a Transaction Audit Dashboard built with Django. It allows users to manage transactions, view analytics, and track transaction history.

## Features
- User authentication (login, registration)
- Add, update, and delete transactions
- View transaction details
- Filter transactions by status and flags
- Search transactions by keywords
- Analytics dashboard for transaction insights
- Transaction history tracking

## Requirements
- Python 3.x
- Django 5.x
- SQLite (or any other database supported by Django)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/tharhtet236401/transaction-audit-dashboard.git
cd transaction-audit-dashboard
```

### 2. Create a Virtual Environment
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
```

or

```bash
virtualenv myenv
myenv\Scripts\activate  # On Windows    
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
- The project uses SQLite by default. You can change the database settings in `auditProject/settings.py` if needed.

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)
To access the Django admin panel, create a superuser:
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Open your browser and go to `http://127.0.0.1:8000/`.

### 8. Access the Application
- Visit the home page to start managing transactions.
- Use the admin panel for advanced management (if you created a superuser).

## Usage
- Users can log in, add transactions, and view analytics.
- The dashboard provides options to filter and view transaction history.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
- Django for the web framework
- SQLite for the database
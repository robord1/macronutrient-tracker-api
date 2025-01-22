
# Macronutrient Tracker API

The Macronutrient Tracker API allows users to set macronutrient goals, log food entries, and retrieve data. It supports user authentication with JWT and provides endpoints to interact with the user's macronutrient data.

## Features

- **User Authentication**:
  - Signup and login with secure password hashing.
  - JWT-based authentication for secure access.

- **Macronutrient Goals**:
  - Set, update, and retrieve personalized macronutrient goals.

- **Food Entries**:
  - Log daily food entries with details about protein, carbs, fat, and sodium.
  - Retrieve food entries by date.

---

## Hosted API

The API is hosted at:  

[https://macronutrient-tracker-api.onrender.com]

---

## Endpoints

### Authentication
- `POST /signup`: Create a new user account.
- `POST /login`: Authenticate a user and retrieve a JWT.

### Goals
- `GET /goals`: Fetch the user's macronutrient goals.
- `POST /goals`: Create new macronutrient goals.
- `PUT /goals`: Update existing macronutrient goals.

### Food Entries
- `POST /food-entries`: Add a new food entry.
- `GET /food-entries`: Retrieve food entries by date.

---

## Installation and Usage

### Prerequisites
- PPython 3.8 or higher
- `pip` for Python package management
- A database (e.g., PostgreSQL or SQLite)

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/robord1/macronutrient-tracker-api.git
   cd macronutrient-tracker-api

2. Install dependencies:

    pip install -r requirements.txt

3. Set up environment variables and database:

    Create a sqlite or postges database  
        
    Link the database by updating the line app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') in app/__init__.py 

4. Initialize the database:

    flask db upgrade

5. Run the application:

    flask run

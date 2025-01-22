import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://strider:a@localhost/mt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key')  # Change this for production

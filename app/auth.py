from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from .models import User
from . import db

auth = Blueprint('auth', __name__)




@auth.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400


        # Validate email format
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email format'}), 400



        # Enforce password strength
        if len(data['password']) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Unable to process your request'}), 409  # Generic message for security

        # Hash the password
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # Create a new user
        new_user = User(email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        # Log the actual error server-side for debugging
        print(f'Error in /signup: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500







@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        

        # Find the user
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401  # Generic error message

        # Create a JWT token
        token = create_access_token(identity=str(user.id))  

        return jsonify({'message': 'Login successful', 'token': token}), 200

    except Exception as e:
        # Log the actual error server-side for debugging
        print(f'Error in /login: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500
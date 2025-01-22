from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from . import db
from .models import FoodEntry
from .models import Goal  
from datetime import datetime  # Import datetime for current date

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    """
    Root endpoint for the Macronutrient Tracker API.
    Provides basic information and confirms the API is running.
    """
    response = {
        "message": "Welcome to the Macronutrient Tracker API!",
        "version": "0.1",
        "status": "online",
        "docs": ""  
    }
    return jsonify(response), 200
    


@main.route('/goals', methods=['GET'])
@jwt_required()  

def get_goals():
    """
    Fetch the goals for the currently authenticated user.
    """
    try:
        # Get the logged-in user's ID from the JWT
        user_id = get_jwt_identity()

        # Fetch all goals for the user
        goals = Goal.query.filter_by(user_id=user_id).all()

        # If no goals are found, return a 404 response
        if not goals:
            return jsonify({"error": "No goals found for this user"}), 404

        # Serialize the goals into a JSON format
        goals_data = [
            {
                "id": goal.id,
                "protein": goal.protein_target,
                "carbs": goal.carbs_target,
                "fat": goal.fat_target,
                "sodium": goal.sodium_target,
            }
            for goal in goals
        ]

        return jsonify({
            "user_id": user_id,
            "goals": goals_data
        }), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching goals: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    

    
@main.route('/goals', methods=['POST', 'PUT'])
@jwt_required()  

def set_goals():
    """
    Update or set goal for the authenticated user.
    """

    user_id = get_jwt_identity()  # Get the logged-in user's ID
    data = request.get_json()  # Parse JSON body from request

    # Validate input
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ['protein', 'carbs', 'fat', 'sodium']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Fetch the user's existing goal (if any)
    goal = Goal.query.filter_by(user_id=user_id).first()

    if not goal:
        # Create new goal
        new_goal = Goal(
            user_id=user_id,
            protein_target=data['protein'],
            carbs_target=data['carbs'],
            fat_target=data['fat'],
            sodium_target=data['sodium']
        )
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({"message": "Goals set successfully"}), 201
    else:
        # Update existing goal
        goal.protein_target = data['protein']
        goal.carbs_target = data['carbs']
        goal.fat_target = data['fat']
        goal.sodium_target = data['sodium']
        db.session.commit()
        return jsonify({"message": "Goals updated successfully"}), 200
        
        
        
        
        
@main.route('/food-entries', methods=['POST'])
@jwt_required()

def add_food_entry():
    """
    Add a new food entry for the authenticated user.
    """

    try:
        # Get the logged-in user's ID
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate input
        required_fields = ['food_name', 'protein', 'carbs', 'fat', 'sodium']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

            # Ensure nutrient values are non-negative numbers
            if field in ['protein', 'carbs', 'fat', 'sodium'] and (
                not isinstance(data[field], (int, float)) or data[field] < 0
            ):
                return jsonify({"error": f"{field} must be a non-negative number"}), 400

        # Validate food_name
        food_name = data['food_name'].strip()
        if not food_name or len(food_name) > 120:
            return jsonify({"error": "food_name must be a non-empty string with a maximum length of 120 characters"}), 400

        # Parse optional date field
        date_param = data.get('date')
        if date_param:
            try:
                entry_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        else:
            entry_date = datetime.utcnow().date()

        # Create a new food entry
        new_entry = FoodEntry(
            user_id=user_id,
            food_name=food_name,
            protein=data['protein'],
            carbs=data['carbs'],
            fat=data['fat'],
            sodium=data['sodium'],
            date=entry_date
        )

        # Save to the database
        db.session.add(new_entry)
        db.session.commit()

        # Return a success message with the new entry details
        return jsonify({
            "message": "Food entry added successfully",
            "food_entry": {
                "id": new_entry.id,
                "food_name": new_entry.food_name,
                "protein": new_entry.protein,
                "carbs": new_entry.carbs,
                "fat": new_entry.fat,
                "sodium": new_entry.sodium,
                "date": new_entry.date.isoformat()
            }
        }), 201

    except Exception as e:
        # Log the error and return a generic error response
        print(f"Error adding food entry: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500





        
@main.route('/food-entries', methods=['GET'])
@jwt_required()  

def get_food_entries():
    """
    Retrieve food entries for the authenticated user, filtered by date or date range.
    """

    user_id = get_jwt_identity()  # Get the logged-in user's ID

    # Parse query parameters
    date_param = request.args.get('date')  
    if date_param:
        try:
            query_date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    else:
        query_date = datetime.utcnow().date()  # Default to today


    # Fetch food entries for the user on the specified date
    entries = FoodEntry.query.filter_by(user_id=user_id, date=query_date).all()

    # Format the results as JSON
    results = [
        {
            "id": entry.id,
            "food_name": entry.food_name,
            "protein": entry.protein,
            "carbs": entry.carbs,
            "fat": entry.fat,
            "sodium": entry.sodium,
            "date": entry.date.strftime('%Y-%m-%d')
        } for entry in entries
    ]

    return jsonify(results), 200

        

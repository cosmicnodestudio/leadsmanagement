from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return {'user': user.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()

        if not data:
            return {'error': 'Request body is required'}, 400

        if 'name' in data:
            user.name = data['name']

        db.session.commit()

        return {
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

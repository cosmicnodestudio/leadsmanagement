from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()

    if not data:
        return {'error': 'Request body is required'}, 400

    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    if not email or not name or not password:
        return {'error': 'Email, name, and password are required'}, 400

    if User.query.filter_by(email=email).first():
        return {'error': 'Email already registered'}, 409

    try:
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return {
            'message': 'User registered successfully',
            'user': user.to_dict()
        }, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()

    if not data:
        return {'error': 'Request body is required'}, 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {'error': 'Email and password are required'}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {'error': 'Invalid email or password'}, 401

    if not user.is_active:
        return {'error': 'User account is inactive'}, 403

    try:
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=str(identity))
        return {
            'message': 'Token refreshed successfully',
            'access_token': access_token
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get current user profile"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return {'user': user.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user"""
    return {'message': 'Logout successful'}, 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()

        if not data:
            return {'error': 'Request body is required'}, 400

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return {'error': 'Old and new passwords are required'}, 400

        if not user.check_password(old_password):
            return {'error': 'Old password is incorrect'}, 401

        user.set_password(new_password)
        db.session.commit()

        return {'message': 'Password changed successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

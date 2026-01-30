from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Lead, LeadInteraction

leads_bp = Blueprint('leads', __name__, url_prefix='/api/leads')

@leads_bp.route('', methods=['GET'])
@jwt_required()
def list_leads():
    """List all leads for current user"""
    try:
        user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None, type=str)

        query = Lead.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'leads': [lead.to_dict() for lead in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@leads_bp.route('', methods=['POST'])
@jwt_required()
def create_lead():
    """Create new lead"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        if not data:
            return {'error': 'Request body is required'}, 400

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return {'error': 'Name and email are required'}, 400

        lead = Lead(
            user_id=user_id,
            name=name,
            email=email,
            phone=data.get('phone'),
            company=data.get('company'),
            source=data.get('source', 'manual'),
            status=data.get('status', 'new'),
            notes=data.get('notes')
        )

        db.session.add(lead)
        db.session.commit()

        return {
            'message': 'Lead created successfully',
            'lead': lead.to_dict()
        }, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@leads_bp.route('/<int:lead_id>', methods=['GET'])
@jwt_required()
def get_lead(lead_id):
    """Get lead details"""
    try:
        user_id = int(get_jwt_identity())
        lead = Lead.query.filter_by(id=lead_id, user_id=user_id).first()

        if not lead:
            return {'error': 'Lead not found'}, 404

        return {'lead': lead.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@leads_bp.route('/<int:lead_id>', methods=['PUT'])
@jwt_required()
def update_lead(lead_id):
    """Update lead"""
    try:
        user_id = int(get_jwt_identity())
        lead = Lead.query.filter_by(id=lead_id, user_id=user_id).first()

        if not lead:
            return {'error': 'Lead not found'}, 404

        data = request.get_json()

        if not data:
            return {'error': 'Request body is required'}, 400

        # Update fields if provided
        if 'name' in data:
            lead.name = data['name']
        if 'email' in data:
            lead.email = data['email']
        if 'phone' in data:
            lead.phone = data['phone']
        if 'company' in data:
            lead.company = data['company']
        if 'status' in data:
            lead.status = data['status']
        if 'source' in data:
            lead.source = data['source']
        if 'notes' in data:
            lead.notes = data['notes']

        db.session.commit()

        return {
            'message': 'Lead updated successfully',
            'lead': lead.to_dict()
        }, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@leads_bp.route('/<int:lead_id>', methods=['DELETE'])
@jwt_required()
def delete_lead(lead_id):
    """Delete lead"""
    try:
        user_id = int(get_jwt_identity())
        lead = Lead.query.filter_by(id=lead_id, user_id=user_id).first()

        if not lead:
            return {'error': 'Lead not found'}, 404

        db.session.delete(lead)
        db.session.commit()

        return {'message': 'Lead deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@leads_bp.route('/search', methods=['GET'])
@jwt_required()
def search_leads():
    """Search leads"""
    try:
        user_id = int(get_jwt_identity())
        query_str = request.args.get('q', '', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if not query_str:
            return {'error': 'Search query is required'}, 400

        query = Lead.query.filter_by(user_id=user_id).filter(
            db.or_(
                Lead.name.ilike(f'%{query_str}%'),
                Lead.email.ilike(f'%{query_str}%'),
                Lead.company.ilike(f'%{query_str}%')
            )
        )

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'leads': [lead.to_dict() for lead in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@leads_bp.route('/<int:lead_id>/interactions', methods=['GET'])
@jwt_required()
def get_lead_interactions(lead_id):
    """Get lead interactions"""
    try:
        user_id = get_jwt_identity()
        lead = Lead.query.filter_by(id=lead_id, user_id=user_id).first()

        if not lead:
            return {'error': 'Lead not found'}, 404

        interactions = LeadInteraction.query.filter_by(lead_id=lead_id).order_by(
            LeadInteraction.created_at.desc()
        ).all()

        return {
            'interactions': [interaction.to_dict() for interaction in interactions]
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@leads_bp.route('/<int:lead_id>/interactions', methods=['POST'])
@jwt_required()
def add_lead_interaction(lead_id):
    """Add lead interaction"""
    try:
        user_id = get_jwt_identity()
        lead = Lead.query.filter_by(id=lead_id, user_id=user_id).first()

        if not lead:
            return {'error': 'Lead not found'}, 404

        data = request.get_json()

        if not data:
            return {'error': 'Request body is required'}, 400

        interaction_type = data.get('interaction_type')
        description = data.get('description')

        if not interaction_type:
            return {'error': 'Interaction type is required'}, 400

        interaction = LeadInteraction(
            lead_id=lead_id,
            user_id=user_id,
            interaction_type=interaction_type,
            description=description
        )

        db.session.add(interaction)
        db.session.commit()

        return {
            'message': 'Interaction added successfully',
            'interaction': interaction.to_dict()
        }, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@leads_bp.route('/interactions/<int:interaction_id>', methods=['DELETE'])
@jwt_required()
def delete_interaction(interaction_id):
    """Delete interaction"""
    try:
        user_id = get_jwt_identity()
        interaction = LeadInteraction.query.filter_by(
            id=interaction_id,
            user_id=user_id
        ).first()

        if not interaction:
            return {'error': 'Interaction not found'}, 404

        db.session.delete(interaction)
        db.session.commit()

        return {'message': 'Interaction deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

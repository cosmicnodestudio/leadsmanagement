from app import db
from datetime import datetime

class Lead(db.Model):
    """Lead model"""
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.Enum('new', 'contacted', 'qualified', 'converted', 'lost'),
        default='new',
        nullable=False,
        index=True
    )
    source = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    interactions = db.relationship('LeadInteraction', backref='lead', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'status': self.status,
            'source': self.source,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class LeadInteraction(db.Model):
    """Lead interaction model"""
    __tablename__ = 'lead_interactions'

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interaction_type = db.Column(
        db.Enum('email', 'call', 'meeting', 'note'),
        nullable=False
    )
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'user_id': self.user_id,
            'interaction_type': self.interaction_type,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
        }

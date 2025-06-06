from datetime import datetime
from app import db

class Project(db.Model):
    """Modelo de projeto do sistema"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)  # 'residential', 'commercial', etc.
    status = db.Column(db.String(20), nullable=False)  # 'estimate', 'approved', 'in_progress', 'completed', 'cancelled'
    installation_address = db.Column(db.String(200), nullable=False)
    installation_city = db.Column(db.String(50), nullable=False)
    installation_state = db.Column(db.String(2), nullable=False)
    installation_zip = db.Column(db.String(10), nullable=False)
    estimated_start_date = db.Column(db.Date)
    estimated_end_date = db.Column(db.Date)
    actual_start_date = db.Column(db.Date)
    actual_end_date = db.Column(db.Date)
    estimated_total = db.Column(db.Numeric(10, 2))
    actual_total = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)
    warranty_period = db.Column(db.Integer)  # em meses
    warranty_end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    estimates = db.relationship('Estimate', backref='project', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='project', lazy='dynamic')
    payments = db.relationship('Payment', backref='project', lazy='dynamic')
    expenses = db.relationship('Expense', backref='project', lazy='dynamic')
    progress = db.relationship('ProjectProgress', backref='project', lazy='dynamic')
    files = db.relationship('File', backref='project', lazy='dynamic')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'title': self.title,
            'project_type': self.project_type,
            'status': self.status,
            'installation_address': self.installation_address,
            'installation_city': self.installation_city,
            'installation_state': self.installation_state,
            'installation_zip': self.installation_zip,
            'estimated_start_date': self.estimated_start_date.isoformat() if self.estimated_start_date else None,
            'estimated_end_date': self.estimated_end_date.isoformat() if self.estimated_end_date else None,
            'actual_start_date': self.actual_start_date.isoformat() if self.actual_start_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'estimated_total': float(self.estimated_total) if self.estimated_total else None,
            'actual_total': float(self.actual_total) if self.actual_total else None,
            'notes': self.notes,
            'warranty_period': self.warranty_period,
            'warranty_end_date': self.warranty_end_date.isoformat() if self.warranty_end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Project {self.title}>'


from datetime import datetime
from app import db

class Schedule(db.Model):
    """Modelo de agendamento do sistema"""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    schedule_type = db.Column(db.String(20), nullable=False)  # 'visit', 'start', 'continuation', 'completion'
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'scheduled', 'completed', 'cancelled', 'rescheduled'
    notes = db.Column(db.Text)
    reminder_sent = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'schedule_type': self.schedule_type,
            'start_datetime': self.start_datetime.isoformat() if self.start_datetime else None,
            'end_datetime': self.end_datetime.isoformat() if self.end_datetime else None,
            'description': self.description,
            'status': self.status,
            'notes': self.notes,
            'reminder_sent': self.reminder_sent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Schedule {self.description}>'


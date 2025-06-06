from datetime import datetime
from app import db

class ProjectProgress(db.Model):
    """Modelo de progresso do projeto do sistema"""
    __tablename__ = 'project_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    progress_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    hours_worked = db.Column(db.Numeric(5, 2), nullable=False)
    area_completed = db.Column(db.Numeric(10, 2))  # em pés quadrados
    percentage_done = db.Column(db.Integer)  # 0-100
    issues = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'progress_date': self.progress_date.isoformat() if self.progress_date else None,
            'description': self.description,
            'hours_worked': float(self.hours_worked) if self.hours_worked else 0,
            'area_completed': float(self.area_completed) if self.area_completed else None,
            'percentage_done': self.percentage_done,
            'issues': self.issues,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<ProjectProgress {self.project_id} - {self.progress_date}>'


class File(db.Model):
    """Modelo de arquivo do sistema"""
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # 'before', 'during', 'after', 'document', etc.
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'file_type': self.file_type,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'description': self.description,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<File {self.file_name}>'


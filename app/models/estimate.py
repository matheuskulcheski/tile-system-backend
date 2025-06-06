from datetime import datetime
from app import db

class Estimate(db.Model):
    """Modelo de orçamento do sistema"""
    __tablename__ = 'estimates'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    estimate_number = db.Column(db.String(20), nullable=False)
    created_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    valid_until = db.Column(db.Date, nullable=False)
    materials_total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    labor_total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    additional_fees = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    discount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    tax_rate = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False)  # 'pending', 'approved', 'rejected'
    notes = db.Column(db.Text)
    terms = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    items = db.relationship('EstimateItem', backref='estimate', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'estimate_number': self.estimate_number,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'materials_total': float(self.materials_total) if self.materials_total else 0,
            'labor_total': float(self.labor_total) if self.labor_total else 0,
            'additional_fees': float(self.additional_fees) if self.additional_fees else 0,
            'discount': float(self.discount) if self.discount else 0,
            'tax_rate': float(self.tax_rate) if self.tax_rate else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'notes': self.notes,
            'terms': self.terms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Estimate {self.estimate_number}>'


class EstimateItem(db.Model):
    """Modelo de item de orçamento do sistema"""
    __tablename__ = 'estimate_items'
    
    id = db.Column(db.Integer, primary_key=True)
    estimate_id = db.Column(db.Integer, db.ForeignKey('estimates.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'material', 'service', 'fee'
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    supplied_by = db.Column(db.String(20), nullable=False)  # 'client', 'company'
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'estimate_id': self.estimate_id,
            'item_type': self.item_type,
            'description': self.description,
            'quantity': float(self.quantity) if self.quantity else 0,
            'unit': self.unit,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0,
            'supplied_by': self.supplied_by,
            'material_id': self.material_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<EstimateItem {self.description}>'


from datetime import datetime
from app import db

class Material(db.Model):
    """Modelo de material do sistema"""
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    material_type = db.Column(db.String(50), nullable=False)  # 'tile', 'grout', 'thinset', 'tool', etc.
    unit = db.Column(db.String(20), nullable=False)  # 'sqft', 'piece', 'box', 'bag', etc.
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    min_stock = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relacionamentos
    estimate_items = db.relationship('EstimateItem', backref='material', lazy='dynamic')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'material_type': self.material_type,
            'unit': self.unit,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'stock_quantity': float(self.stock_quantity) if self.stock_quantity else 0,
            'min_stock': float(self.min_stock) if self.min_stock else 0,
            'supplier_id': self.supplier_id,
            'notes': self.notes,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Material {self.name}>'


class Supplier(db.Model):
    """Modelo de fornecedor do sistema"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relacionamentos
    materials = db.relationship('Material', backref='supplier', lazy='dynamic')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'notes': self.notes,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Supplier {self.name}>'


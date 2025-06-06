from datetime import datetime
from app import db

class Payment(db.Model):
    """Modelo de pagamento do sistema"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # 'cash', 'check', 'credit_card', 'transfer', etc.
    reference = db.Column(db.String(100))  # número do cheque, confirmação de transferência, etc.
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'amount': float(self.amount) if self.amount else 0,
            'payment_method': self.payment_method,
            'reference': self.reference,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.amount}>'


class Expense(db.Model):
    """Modelo de despesa do sistema"""
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'material', 'labor', 'transportation', etc.
    payment_method = db.Column(db.String(50), nullable=False)  # 'cash', 'check', 'credit_card', etc.
    receipt_file = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'expense_date': self.expense_date.isoformat() if self.expense_date else None,
            'description': self.description,
            'amount': float(self.amount) if self.amount else 0,
            'category': self.category,
            'payment_method': self.payment_method,
            'receipt_file': self.receipt_file,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Expense {self.description} - {self.amount}>'


from datetime import datetime, timedelta
from app import db
from app.models.user import User
from app.models.client import Client
from app.models.project import Project
from app.models.material import Material, Supplier

def init_db():
    """Inicializa o banco de dados com dados de exemplo"""
    # Limpa o banco de dados
    db.drop_all()
    db.create_all()
    
    # Cria usuários de exemplo
    owner = User(
        name='John Smith',
        email='owner@tilesystem.com',
        role='owner',
        phone='555-123-4567'
    )
    owner.password = 'password123'
    
    installer = User(
        name='Mike Johnson',
        email='installer@tilesystem.com',
        role='installer',
        phone='555-987-6543'
    )
    installer.password = 'password123'
    
    db.session.add_all([owner, installer])
    db.session.commit()
    
    # Cria clientes de exemplo
    client1 = Client(
        name='Robert Williams',
        email='robert@example.com',
        phone='555-111-2222',
        address='123 Palm Ave',
        city='Miami',
        state='FL',
        zip_code='33101',
        referral_source='Google',
        notes='Prefers communication via email'
    )
    
    client2 = Client(
        name='Jennifer Davis',
        email='jennifer@example.com',
        phone='555-333-4444',
        address='456 Ocean Dr',
        city='Fort Lauderdale',
        state='FL',
        zip_code='33301',
        referral_source='Friend Referral',
        notes='Prefers communication via phone'
    )
    
    client3 = Client(
        name='Michael Brown',
        email='michael@example.com',
        phone='555-555-6666',
        address='789 Beach Blvd',
        city='Jacksonville',
        state='FL',
        zip_code='32202',
        referral_source='Website',
        notes='Has multiple properties'
    )
    
    db.session.add_all([client1, client2, client3])
    db.session.commit()
    
    # Cria projetos de exemplo
    project1 = Project(
        client_id=client1.id,
        title='Kitchen Backsplash Installation',
        project_type='residential',
        status='in_progress',
        installation_address='123 Palm Ave',
        installation_city='Miami',
        installation_state='FL',
        installation_zip='33101',
        estimated_start_date=datetime.now().date(),
        estimated_end_date=(datetime.now() + timedelta(days=3)).date(),
        estimated_total=1200.00,
        notes='Subway tile backsplash, approximately 30 sqft'
    )
    
    project2 = Project(
        client_id=client2.id,
        title='Master Bathroom Renovation',
        project_type='residential',
        status='estimate',
        installation_address='456 Ocean Dr',
        installation_city='Fort Lauderdale',
        installation_state='FL',
        installation_zip='33301',
        estimated_start_date=(datetime.now() + timedelta(days=7)).date(),
        estimated_end_date=(datetime.now() + timedelta(days=14)).date(),
        estimated_total=3500.00,
        notes='Complete bathroom tile renovation, floor and walls'
    )
    
    project3 = Project(
        client_id=client3.id,
        title='Office Lobby Floor',
        project_type='commercial',
        status='completed',
        installation_address='789 Business Center',
        installation_city='Jacksonville',
        installation_state='FL',
        installation_zip='32202',
        estimated_start_date=(datetime.now() - timedelta(days=14)).date(),
        estimated_end_date=(datetime.now() - timedelta(days=7)).date(),
        actual_start_date=(datetime.now() - timedelta(days=14)).date(),
        actual_end_date=(datetime.now() - timedelta(days=6)).date(),
        estimated_total=5000.00,
        actual_total=5200.00,
        notes='Porcelain tile installation in office lobby, approximately 500 sqft',
        warranty_period=12,
        warranty_end_date=(datetime.now() + timedelta(days=359)).date()
    )
    
    db.session.add_all([project1, project2, project3])
    db.session.commit()
    
    # Cria fornecedores de exemplo
    supplier1 = Supplier(
        name='Florida Tile Supply',
        contact_person='David Wilson',
        phone='555-777-8888',
        email='david@floridasupply.com',
        address='100 Supply St',
        city='Orlando',
        state='FL',
        zip_code='32801',
        notes='Main supplier for ceramic and porcelain tiles'
    )
    
    supplier2 = Supplier(
        name='Grout & More',
        contact_person='Sarah Johnson',
        phone='555-999-0000',
        email='sarah@groutmore.com',
        address='200 Material Ave',
        city='Tampa',
        state='FL',
        zip_code='33601',
        notes='Supplier for grout, thinset, and other materials'
    )
    
    db.session.add_all([supplier1, supplier2])
    db.session.commit()
    
    # Cria materiais de exemplo
    material1 = Material(
        name='White Subway Tile',
        description='3x6 inch white ceramic subway tile',
        material_type='tile',
        unit='sqft',
        unit_price=3.99,
        stock_quantity=200,
        min_stock=50,
        supplier_id=supplier1.id
    )
    
    material2 = Material(
        name='Porcelain Floor Tile',
        description='12x24 inch gray porcelain floor tile',
        material_type='tile',
        unit='sqft',
        unit_price=4.50,
        stock_quantity=300,
        min_stock=100,
        supplier_id=supplier1.id
    )
    
    material3 = Material(
        name='Premium Thinset',
        description='50lb bag of premium thinset mortar',
        material_type='thinset',
        unit='bag',
        unit_price=22.99,
        stock_quantity=40,
        min_stock=10,
        supplier_id=supplier2.id
    )
    
    material4 = Material(
        name='Sanded Grout',
        description='10lb bag of sanded grout, various colors',
        material_type='grout',
        unit='bag',
        unit_price=15.99,
        stock_quantity=30,
        min_stock=5,
        supplier_id=supplier2.id
    )
    
    db.session.add_all([material1, material2, material3, material4])
    db.session.commit()
    
    print('Database initialized with example data')


if __name__ == '__main__':
    # Este script pode ser executado diretamente
    from app import create_app
    app = create_app()
    with app.app_context():
        init_db()


from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
    """Esquema para validação e serialização de projetos"""
    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    project_type = fields.Str(required=True, validate=validate.OneOf([
        'residential', 'commercial', 'renovation', 'new_construction', 'other'
    ]))
    status = fields.Str(required=True, validate=validate.OneOf([
        'estimate', 'approved', 'in_progress', 'completed', 'cancelled'
    ]))
    installation_address = fields.Str(required=True, validate=validate.Length(max=200))
    installation_city = fields.Str(required=True, validate=validate.Length(max=50))
    installation_state = fields.Str(required=True, validate=validate.Length(equal=2))
    installation_zip = fields.Str(required=True, validate=validate.Length(max=10))
    estimated_start_date = fields.Date()
    estimated_end_date = fields.Date()
    actual_start_date = fields.Date()
    actual_end_date = fields.Date()
    estimated_total = fields.Decimal(as_string=True)
    actual_total = fields.Decimal(as_string=True)
    notes = fields.Str()
    warranty_period = fields.Int()
    warranty_end_date = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProjectUpdateSchema(Schema):
    """Esquema para atualização de projetos"""
    client_id = fields.Int()
    title = fields.Str(validate=validate.Length(min=2, max=100))
    project_type = fields.Str(validate=validate.OneOf([
        'residential', 'commercial', 'renovation', 'new_construction', 'other'
    ]))
    status = fields.Str(validate=validate.OneOf([
        'estimate', 'approved', 'in_progress', 'completed', 'cancelled'
    ]))
    installation_address = fields.Str(validate=validate.Length(max=200))
    installation_city = fields.Str(validate=validate.Length(max=50))
    installation_state = fields.Str(validate=validate.Length(equal=2))
    installation_zip = fields.Str(validate=validate.Length(max=10))
    estimated_start_date = fields.Date()
    estimated_end_date = fields.Date()
    actual_start_date = fields.Date()
    actual_end_date = fields.Date()
    estimated_total = fields.Decimal(as_string=True)
    actual_total = fields.Decimal(as_string=True)
    notes = fields.Str()
    warranty_period = fields.Int()
    warranty_end_date = fields.Date()


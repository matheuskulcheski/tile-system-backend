from marshmallow import Schema, fields, validate

class EstimateItemSchema(Schema):
    """Esquema para validação e serialização de itens de orçamento"""
    id = fields.Int(dump_only=True)
    estimate_id = fields.Int(dump_only=True)
    item_type = fields.Str(required=True, validate=validate.OneOf(['material', 'service', 'fee']))
    description = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    quantity = fields.Decimal(required=True, as_string=True)
    unit = fields.Str(required=True, validate=validate.Length(max=20))
    unit_price = fields.Decimal(required=True, as_string=True)
    total_price = fields.Decimal(required=True, as_string=True)
    supplied_by = fields.Str(required=True, validate=validate.OneOf(['client', 'company']))
    material_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class EstimateSchema(Schema):
    """Esquema para validação e serialização de orçamentos"""
    id = fields.Int(dump_only=True)
    project_id = fields.Int(required=True)
    estimate_number = fields.Str(required=True, validate=validate.Length(max=20))
    created_date = fields.Date(required=True)
    valid_until = fields.Date(required=True)
    materials_total = fields.Decimal(as_string=True)
    labor_total = fields.Decimal(as_string=True)
    additional_fees = fields.Decimal(as_string=True)
    discount = fields.Decimal(as_string=True)
    tax_rate = fields.Decimal(as_string=True)
    tax_amount = fields.Decimal(as_string=True)
    total_amount = fields.Decimal(as_string=True)
    status = fields.Str(required=True, validate=validate.OneOf(['pending', 'approved', 'rejected']))
    notes = fields.Str()
    terms = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    items = fields.List(fields.Nested(EstimateItemSchema), dump_only=True)


class EstimateUpdateSchema(Schema):
    """Esquema para atualização de orçamentos"""
    project_id = fields.Int()
    estimate_number = fields.Str(validate=validate.Length(max=20))
    created_date = fields.Date()
    valid_until = fields.Date()
    materials_total = fields.Decimal(as_string=True)
    labor_total = fields.Decimal(as_string=True)
    additional_fees = fields.Decimal(as_string=True)
    discount = fields.Decimal(as_string=True)
    tax_rate = fields.Decimal(as_string=True)
    tax_amount = fields.Decimal(as_string=True)
    total_amount = fields.Decimal(as_string=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'approved', 'rejected']))
    notes = fields.Str()
    terms = fields.Str()


class EstimateWithItemsSchema(EstimateSchema):
    """Esquema para orçamentos com itens incluídos"""
    items = fields.List(fields.Nested(EstimateItemSchema))


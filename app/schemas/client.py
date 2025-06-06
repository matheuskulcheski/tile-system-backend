from marshmallow import Schema, fields, validate, validates, ValidationError
from email_validator import validate_email, EmailNotValidError

class ClientSchema(Schema):
    """Esquema para validação e serialização de clientes"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(allow_none=True)
    phone = fields.Str(required=True, validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=200))
    city = fields.Str(validate=validate.Length(max=50))
    state = fields.Str(validate=validate.Length(equal=2))
    zip_code = fields.Str(validate=validate.Length(max=10))
    referral_source = fields.Str(validate=validate.Length(max=100))
    notes = fields.Str()
    active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('email')
    def validate_email(self, value):
        if value:
            try:
                validate_email(value)
            except EmailNotValidError as e:
                raise ValidationError(str(e))


class ClientUpdateSchema(Schema):
    """Esquema para atualização de clientes"""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email(allow_none=True)
    phone = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=200))
    city = fields.Str(validate=validate.Length(max=50))
    state = fields.Str(validate=validate.Length(equal=2))
    zip_code = fields.Str(validate=validate.Length(max=10))
    referral_source = fields.Str(validate=validate.Length(max=100))
    notes = fields.Str()
    active = fields.Bool()
    
    @validates('email')
    def validate_email(self, value):
        if value:
            try:
                validate_email(value)
            except EmailNotValidError as e:
                raise ValidationError(str(e))


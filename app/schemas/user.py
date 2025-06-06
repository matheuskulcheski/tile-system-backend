from marshmallow import Schema, fields, validate, validates, ValidationError
from email_validator import validate_email, EmailNotValidError

class UserSchema(Schema):
    """Esquema para validação e serialização de usuários"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(required=True, validate=validate.OneOf(['owner', 'installer']))
    phone = fields.Str(validate=validate.Length(max=20))
    active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('email')
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError(str(e))


class UserUpdateSchema(Schema):
    """Esquema para atualização de usuários"""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    role = fields.Str(validate=validate.OneOf(['owner', 'installer']))
    phone = fields.Str(validate=validate.Length(max=20))
    active = fields.Bool()
    
    @validates('email')
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError(str(e))


class PasswordChangeSchema(Schema):
    """Esquema para alteração de senha"""
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))
    confirm_password = fields.Str(required=True)
    
    @validates('confirm_password')
    def validate_confirm_password(self, value):
        if value != self.context.get('new_password'):
            raise ValidationError('As senhas devem ser iguais')


class LoginSchema(Schema):
    """Esquema para login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


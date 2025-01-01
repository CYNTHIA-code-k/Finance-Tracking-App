from marshmallow import Schema, fields

class BudgetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    amount = fields.Float(required=True)
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)

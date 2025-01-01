from marshmallow import Schema, fields, validate

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(['income', 'expense']))
    category = fields.Str(required=True)
    date = fields.DateTime(dump_only=True)
    is_recurring = fields.Boolean()
    recurring_frequency = fields.Str(validate=validate.OneOf(['weekly', 'monthly', 'yearly']))
    tags = fields.List(fields.Str())
    location = fields.Str()
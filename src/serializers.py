from marshmallow import Schema, fields, validate, EXCLUDE


class UserSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=1), load_only=True)

    public_id = fields.Str(dump_only=True, data_key='id')
    email = fields.Email(required=True)
    first_name = fields.Str(validate=validate.Length(max=126))
    last_name = fields.Str(validate=validate.Length(max=126))

    class Meta:
        unknown = EXCLUDE
        ordered = True

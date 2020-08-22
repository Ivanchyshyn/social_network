from marshmallow import Schema, fields, validate, EXCLUDE


class UserSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=1), load_only=True)

    public_id = fields.Str(data_key='id', dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(validate=validate.Length(max=126))
    last_name = fields.Str(validate=validate.Length(max=126))

    class Meta:
        unknown = EXCLUDE
        ordered = True


class PostSchema(Schema):
    public_id = fields.Str(data_key='id', dump_only=True)
    author = fields.Nested(UserSchema, allow_none=True, dump_only=True)
    text = fields.Str(required=True)
    users_liked_count = fields.Integer(data_key='likes', dump_only=True)

    class Meta:
        unknown = EXCLUDE
        ordered = True


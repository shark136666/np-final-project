from marshmallow import fields, Schema

from api.base import RequestDto


class RequestCreateUserDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)


class RequestCreatemeaasgeDto(RequestDto):
    __schema__ = RequestCreateUserDtoSchema

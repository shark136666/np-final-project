import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResponseDto


class ResponseMessageDtoSchema(Schema):
    id = fields.Int(required=True)
    sender_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    update_at = fields.DateTime(required=True)
    recipient_id = fields.Int(required=True)
    message = fields.Str(required=True)

    @pre_load
    @post_load
    def deserialize_datetime(self, data: dict, *args, **kwargs) -> dict:

        if 'created_at' in data:
            data['created_at'] = self.datetime_to_iso(data['created_at'])

        if 'update_at' in data:
            data['update_at'] = self.datetime_to_iso(data['update_at'])

        return data

    @staticmethod
    def datetime_to_iso(data):
        if isinstance(data, datetime.datetime):
            return data.isoformat()

        return data


class ResponseMessageDto(ResponseDto, ResponseMessageDtoSchema):
    __schema__ = ResponseMessageDtoSchema

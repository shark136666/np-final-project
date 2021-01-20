from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateUserDto
from transport.sanic.endpoints import BaseEndpoint
from api.response import ResponseUserDto
from transport.sanic.exceptions import SanicPasswordHashException,SanicDBException,SanicEmployeeConflictException


from db.queries import user as user_queries
from db.exceptions import DBDataException,DBintegrityException,DBEmployeeExistException
from helpers.password import generate_hash
from helpers.password import GeneratePasswordHashException


class CreateUserEndpoint(BaseEndpoint):
    async def method_post(self, request: Request, body: dict,session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
        except GeneratePasswordHashException as e:
            raise SanicPasswordHashException(str(e))

        try:
            db_user = user_queries.create_user(session, request_model, hashed_password)
        except DBEmployeeExistException as e:
            raise SanicEmployeeConflictException('Login is busy')
        try:
            session.commit_session()
        except (DBDataException, DBintegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(body=response_model.dump(), status=201)
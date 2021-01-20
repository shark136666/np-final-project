from api.request import RequestCreateUserDto
from db.database import DBSession
from db.exceptions import DBEmployeeExistException, DBEmployeeNotExistExtension
from db.models import DBUser


def create_user(session: DBSession, user: RequestCreateUserDto, hashed_password: bytes) -> DBUser:
    new_user = DBUser(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    if session.get_user_login(new_user.login) is not None:
        raise DBEmployeeExistException
    session.add_model(new_user)
    return new_user


def get_user(session: DBSession, login: str = str, user_id: int = None) -> DBUser:
    db_user = None

    if login is not None:
        db_user = session.get_user_login(login)
    elif user_id is not None:
        db_user = session.get_user_by_id(user_id)

    if db_user is None:
        raise DBEmployeeExistException

    return db_user

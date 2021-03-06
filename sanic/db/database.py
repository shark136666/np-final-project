from typing import List

from sqlalchemy import and_
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBUser, DBMessage


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)

    def close_session(self):
        self.close_session()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_user_login(self, login: str) -> DBUser:
        return self._session.query(DBUser).filter(DBUser.login == login).first()

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()

    def get_user_by_id(self, user_id: int):
        return self._session.query(DBUser).filter(and_(
            DBUser.id == user_id, DBUser.is_delete == False)).first()

    def get_user_id_by_login(self, login: str):
        return self._session.query(DBUser).filter(
            and_(DBUser.login == login, DBUser.is_delete == False)).first().id

    def get_message(self, message_id):
        return self._session.query(DBMessage).filter(
            and_(DBMessage.id == message_id, DBMessage.is_delete == False)).first()

    def get_all_messages(self, sender_id) -> List[DBMessage]:
        return self._session.query(DBMessage).filter(
            and_(DBMessage.sender_id == sender_id, DBMessage.is_delete == False)).all()


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)

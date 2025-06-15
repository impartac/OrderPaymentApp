from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

class BaseORM(DeclarativeBase):
    metadata = MetaData()
    __table_args__ = {'info': {'is_async': True}}

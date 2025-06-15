from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession

from Domain.Repositories.repository_interface import RepositoryInterface


class BaseRepository(RepositoryInterface, ABC):
    _session : AsyncSession

    def __init__(self, session : AsyncSession):
        self._session = session

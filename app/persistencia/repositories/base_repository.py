from typing import Any, TypeVar

from sqlalchemy.orm import Session

from app.persistencia.database import SessionLocal

T = TypeVar("T")


class BaseRepository:
    def __init__(self, model_class: type[T], session: Session | None = None):
        self.model_class = model_class
        self._session = session

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = SessionLocal()
        return self._session

    def get_by_id(self, entity_id: int) -> T | None:
        return self.session.query(self.model_class).filter_by(id=entity_id).first()

    def list_all(self) -> list[T]:
        return self.session.query(self.model_class).all()

    def create(self, **kwargs: Any) -> T:
        entity = self.model_class(**kwargs)
        self.session.add(entity)
        self.session.commit()
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False

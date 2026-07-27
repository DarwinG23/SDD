from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.persistencia.database import Base


class Fenomeno(Base):
    __tablename__ = "fenomenos"

    id_fenomeno = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=False)
    estado = Column(Boolean, default=True)

    rangos = relationship("Rango", back_populates="fenomeno")

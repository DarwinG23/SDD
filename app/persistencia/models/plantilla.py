from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.persistencia.database import Base


class Plantilla(Base):
    __tablename__ = "plantillas"

    id_plantilla = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    lenguaje = Column(String(50), nullable=False)
    version = Column(String(50), nullable=False)
    objetivo = Column(String(500), nullable=False)
    salida = Column(String(500), nullable=False)
    frameworck = Column(String(100), nullable=False)

    promts = relationship("Promt", back_populates="plantilla")

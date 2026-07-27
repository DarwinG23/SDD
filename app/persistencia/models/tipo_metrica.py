from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.persistencia.database import Base


class TipoMetrica(Base):
    __tablename__ = "tipos_metrica"

    id_tipo_metrica = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=False)
    unidad = Column(String(50), nullable=False)

    mediciones = relationship("Medicion", back_populates="tipo_metrica")
    rangos = relationship("Rango", back_populates="tipo_metrica")

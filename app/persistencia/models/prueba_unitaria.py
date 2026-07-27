from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.persistencia.database import Base


class PruebaUnitaria(Base):
    __tablename__ = "pruebas_unitarias"

    id_prueba_unitaria = Column(Integer, primary_key=True, autoincrement=True)
    codigo_prueba = Column(String(10000), nullable=False)
    estado = Column(String(50), nullable=False)
    detalle = Column(String(2000), nullable=False)
    salida_esperada = Column(String(2000), nullable=False)
    id_codigo_fuente = Column(Integer, ForeignKey("codigos_fuente.id_codigo_fuente"), nullable=False)

    codigo_fuente = relationship("CodigoFuente", back_populates="pruebas")

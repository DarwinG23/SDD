from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.persistencia.database import Base


class CodigoFuente(Base):
    __tablename__ = "codigos_fuente"

    id_codigo_fuente = Column(Integer, primary_key=True, autoincrement=True)
    nombre_archivo = Column(String(255), nullable=False)
    contenido = Column(String(10000), nullable=False)
    lenguaje = Column(String(50), nullable=False)
    numero_lineas = Column(Integer, nullable=False)
    validado = Column(Boolean, default=False)
    id_promt = Column(Integer, ForeignKey("promts.id_promt"), nullable=False)

    promt = relationship("Promt", back_populates="codigos_fuente")
    pruebas = relationship("PruebaUnitaria", back_populates="codigo_fuente")
    evaluaciones = relationship("Evaluacion", back_populates="codigo_fuente")

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.persistencia.database import Base


class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id_evaluacion = Column(Integer, primary_key=True, autoincrement=True)
    resultado = Column(Boolean, nullable=False)
    detalle = Column(String(2000), nullable=False)
    cobertura = Column(Float, nullable=True)
    mutation_score = Column(Float, nullable=True)
    failure_detection = Column(Float, nullable=True)
    all_passed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    id_codigo_fuente = Column(Integer, ForeignKey("codigos_fuente.id_codigo_fuente"), nullable=False)
    id_reporte = Column(Integer, ForeignKey("reportes.id_reporte"), nullable=True)

    codigo_fuente = relationship("CodigoFuente", back_populates="evaluaciones")
    mediciones = relationship("Medicion", back_populates="evaluacion")
    reporte = relationship("Reporte", back_populates="evaluacion", uselist=False)

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.persistencia.database import Base


class Medicion(Base):
    __tablename__ = "mediciones"

    id_medicion = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    id_evaluacion = Column(Integer, ForeignKey("evaluaciones.id_evaluacion"), nullable=False)
    id_tipo_metrica = Column(Integer, ForeignKey("tipos_metrica.id_tipo_metrica"), nullable=False)

    evaluacion = relationship("Evaluacion", back_populates="mediciones")
    tipo_metrica = relationship("TipoMetrica", back_populates="mediciones")

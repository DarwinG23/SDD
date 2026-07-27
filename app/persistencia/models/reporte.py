from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime

from app.persistencia.database import Base


class Reporte(Base):
    __tablename__ = "reportes"

    id_reporte = Column(Integer, primary_key=True, autoincrement=True)
    formato = Column(String(50), default="pdf")
    fecha_generacion = Column(DateTime, default=datetime.now)
    detalle = Column(String(2000), nullable=False)
    pdf_data = Column(LargeBinary, nullable=True)

    evaluacion = relationship("Evaluacion", back_populates="reporte")

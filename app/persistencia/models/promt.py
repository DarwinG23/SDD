from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.persistencia.database import Base


class Promt(Base):
    __tablename__ = "promts"

    id_promt = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(String(2000), nullable=False)
    objetivo = Column(String(500), nullable=False)
    detalle = Column(String(2000), nullable=False)
    id_plantilla = Column(Integer, ForeignKey("plantillas.id_plantilla"), nullable=False)

    plantilla = relationship("Plantilla", back_populates="promts")
    codigos_fuente = relationship("CodigoFuente", back_populates="promt")

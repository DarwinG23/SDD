from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.persistencia.database import Base


class Rango(Base):
    __tablename__ = "rangos"

    id_rango = Column(Integer, primary_key=True, autoincrement=True)
    limite_inferior = Column(Float, nullable=False)
    limite_superior = Column(Float, nullable=False)
    id_tipo_metrica = Column(Integer, ForeignKey("tipos_metrica.id_tipo_metrica"), nullable=False)
    id_fenomeno = Column(Integer, ForeignKey("fenomenos.id_fenomeno"), nullable=False)

    tipo_metrica = relationship("TipoMetrica", back_populates="rangos")
    fenomeno = relationship("Fenomeno", back_populates="rangos")

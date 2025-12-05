from sqlalchemy import Column, Integer, LargeBinary
from app.database import Base

class Face(Base):
    __tablename__ = 'faces'
    id_face = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer)
    descriptor = Column(LargeBinary)
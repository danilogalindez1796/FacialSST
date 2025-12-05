from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 🔹 CONEXIÓN A SUPABASE - ACTUALIZADA
DATABASE_URL = "postgresql://postgres.aiuqnhdflqoojhbmbxvl:pu41S447fN0F7gi9@aws-1-us-east-2.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
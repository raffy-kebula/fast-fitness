from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import PASSWORD

db_url = f"postgresql://raffy:{PASSWORD}@localhost:5432/fitness"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT version();"))
#         version = result.fetchone()
#         print("Successfully connection. \nVersion PostgreSQL:", version[0])
# except Exception as e:
#     print("Error connection:", e)
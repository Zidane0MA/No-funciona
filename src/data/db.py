from src.models.graficas import Graficas
from sqlmodel import SQLModel, Session, create_engine

db_user: str = "zidan"  
db_password: str = "1234"
db_server: str = "fastapi-db" 
db_port: int = 3306  
db_name: str = "graficasdb" 

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Graficas(modelo="ABC-1234", serie="Nvidia RTX 4050", precio="500"))
        session.add(Graficas(modelo="XYZ-5678", serie="Nvidia RTX 5090", precio="5000"))
        session.add(Graficas(modelo="LMN-9101", serie="Nvidia GTX 750", precio="300"))
        session.add(Graficas(modelo="DEF-2345", serie="Nvidia RTX 4080 Super", precio="3000"))
        session.add(Graficas(modelo="GHI-6789", serie="Nvidia RTX 3090 TI", precio="3500"))
        session.add(Graficas(modelo="JKL-3456", serie="Nvidia H200", precio="99999"))
        session.commit()

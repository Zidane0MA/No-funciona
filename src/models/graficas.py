from sqlmodel import SQLModel, Field

class Graficas(SQLModel, table=True):
    modelo: str | None = Field(default=None, primary_key=True)
    serie: str = Field(index=True, max_length=50)
    precio: int = Field(nullable=True)
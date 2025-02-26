from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy import asc
from contextlib import asynccontextmanager
from typing import Annotated

from src.models.graficas import Graficas
from src.data.db import get_session, init_db

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)

@app.get("/")
def bienvenida():
    return { "mensaje": "Bienvenido a la base de datos de la tienda de graficas de zidan"}

@app.get("/graficas", response_model=list[Graficas])
def lista_graficas(session: SessionDep):
    graficas = session.exec(select(Graficas)).all()
    return graficas

@app.post("/graficas", response_model=Graficas)
def nuevo_graficas(graficas: Graficas, session: SessionDep):
    graficas_encontrado = session.get(Graficas, graficas.modelo)
    if graficas_encontrado:
        raise HTTPException(status_code=400, detail="Modelo de grafica existente")
    session.add(graficas)
    session.commit()
    session.refresh(graficas)
    return graficas

@app.get("/graficas/{serie}", response_model=Graficas)
def lista_graficas(serie: str, session: SessionDep):
    graficas_encontrado = session.get(Graficas, serie)
    if not graficas_encontrado:
        raise HTTPException(status_code=404, detail="Serie de grafica no encontrada")
    return graficas_encontrado

@app.delete("/borrar/{modelo}")
def borrar(modelo: str, session: SessionDep):
    graficas_encontrado = session.get(Graficas, modelo)
    if not graficas_encontrado:
        raise HTTPException(status_code=404, detail="Modelo de grafica no encontrado")
    session.delete(graficas_encontrado)
    session.commit()
    return {"mensaje": "Modelo de grafica eliminado"}

@app.put("/cambiar", response_model=Graficas)
def cambia_modelo(graficas: Graficas, session: SessionDep):
    graficas_encontrado = session.get(Graficas, graficas.modelo)
    if not graficas_encontrado:
        raise HTTPException(status_code=404, detail="modelo de grafica no encontrado")
    graficas_data = graficas.model_dump(exclude_unset=True)
    graficas_encontrado.sqlmodel_update(graficas_data)
    session.add(graficas_encontrado)
    session.commit()
    session.refresh(graficas_encontrado)
    return graficas_encontrado
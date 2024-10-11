from typing import Optional, Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, SQLModel

    

class Puffles(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    nome: str = Field(index=True)
    descricao: str
    custo: int = Field(index=True)
    data_lancamento: str = Field(index=True)
    imagem: str
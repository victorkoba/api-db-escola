from pydantic import BaseModel
from typing import Optional
from datetime import date

class EstadoBase(BaseModel):
    nome_estado: str
    sigla_estado: str

class EstadoCreate(EstadoBase):
    pass

class EstadoResponse(EstadoBase):
    cod_estado: int

    class Config:
        from_attributes = True


class CidadeBase(BaseModel):
    nome_cidade: str
    cod_estado: int

class CidadeCreate(CidadeBase):
    pass

class CidadeResponse(CidadeBase):
    cod_cidade: int

    class Config:
        from_attributes = True
        
class AlunoBase(BaseModel):
    nome_aluno: str
    email_aluno: Optional[str] = None
    idade_aluno: Optional[int] = None
    cod_cidade: int
    data_cadastro_aluno: date
    ativo_aluno: bool = True

class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(AlunoBase):
    cod_aluno: int
    
    class Config:
        from_attributes = True

class CursoBase(BaseModel):
    nome_curso: str
    carga_horaria_curso: int
    preco_curso: float

class CursoCreate(CursoBase):
    pass

class CursoResponse(CursoBase):
    cod_curso: int

    class Config:
        from_attributes = True
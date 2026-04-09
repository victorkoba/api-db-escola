from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Numeric
from app.database import Base

class Estado(Base):
    __tablename__ = "tb_estados"

    cod_estado = Column(Integer, primary_key=True, index=True)
    nome_estado = Column(String(50), nullable=False)
    sigla_estado = Column(String(2), nullable=False)

class Cidade(Base):
    __tablename__ = "tb_cidades"

    cod_cidade = Column(Integer, primary_key=True, index=True)
    nome_cidade = Column(String(100), nullable=False)
    cod_estado = Column(Integer, ForeignKey("tb_estados.cod_estado"), nullable=False)
    
class Aluno(Base):
    __tablename__ = "tb_alunos"
    
    cod_aluno = Column(Integer, primary_key=True, index=True)
    nome_aluno = Column(String(100), nullable=False)
    email_aluno = Column(String(100), nullable=True)
    idade_aluno = Column(Integer, nullable=True)
    cod_cidade = Column(Integer, ForeignKey("tb_cidades.cod_cidade"), nullable=False)
    data_cadastro_aluno = Column(Date, nullable=False)
    ativo_aluno = Column(Boolean, nullable=False, default=True)
    
class Curso(Base):
    __tablename__ = "tb_cursos"

    cod_curso = Column(Integer, primary_key=True, index=True)
    nome_curso = Column(String(100), nullable=False)
    carga_horaria_curso = Column(Integer, nullable=False)
    preco_curso = Column(Numeric(10,2), nullable=False)
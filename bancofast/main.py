from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Sistema Escolar", \
description="Operações do banco bd_escola")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para Criar um novo Registro (POST)
@app.post("/estados/", response_model=schemas.EstadoResponse, status_code=201)
def criar_estado(estado: schemas.EstadoCreate, db: Session = Depends(get_db)):
    novo_estado = models.Estado(
        nome_estado=estado.nome_estado,
        sigla_estado=estado.sigla_estado
    )
    db.add(novo_estado)
    db.commit()
    db.refresh(novo_estado)
    return novo_estado

# Rota para Listar todos os Registros (GET)
@app.get("/estados/", response_model=List[schemas.EstadoResponse])
def listar_estados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lista = db.query(models.Estado).offset(skip).limit(limit).all()
    return lista

# Rota para Buscar um Registro Específico (GET)
@app.get("/estados/{cod_estado}", response_model=schemas.EstadoResponse)
def buscar_estado(cod_estado: int, db: Session = Depends(get_db)):
    estado = db.query(models.Estado).filter(models.Estado.cod_estado == cod_estado).first()
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado Inexistente.")
    return estado

# Rota para Atualizar um Registro (PUT)
@app.put("/estados/{cod_estado}", response_model=schemas.EstadoResponse)
def atualizar_estado(cod_estado: int, estado_novo: schemas.EstadoCreate, db: Session = Depends(get_db)):
    estado = db.query(models.Estado).filter(models.Estado.cod_estado == cod_estado).first()
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado Inexistente.")
    
    estado.nome_estado = estado_novo.nome_estado
    estado.sigla_estado = estado_novo.sigla_estado
    
    db.commit()
    db.refresh(estado)
    return estado

# Rota para Excluir um Registro (DELETE)
@app.delete("/estados/{cod_estado}", status_code=204)
def deletar_estado(cod_estado: int, db: Session = Depends(get_db)):
    estado = db.query(models.Estado).filter(models.Estado.cod_estado == cod_estado).first()
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado Inexistente.")
    
    db.delete(estado)
    db.commit()
    return None
    
# ==========================================
# ROTAS DA TABELA CIDADES
# ==========================================

# Rota para Criar Cidade (Regra Forte e Estratégica Inserida)
@app.post("/cidades/", response_model=schemas.CidadeResponse, status_code=201)
def criar_cidade(cidade: schemas.CidadeCreate, db: Session = Depends(get_db)):
    
    # Validação Ativa de Regra Mestre Categórica
    # Ordem: Buscar conferir se o numero de preenchimento relatado bate em algum registro de Estado
    estado_existe = db.query(models.Estado).filter(models.Estado.cod_estado == cidade.cod_estado).first()
    
    # Se bater no banco remoto e retornar em vazio silencioso da busca, barramos o processo e o próprio usuário sem forçar o banco.
    if estado_existe is None:
        raise HTTPException(
            status_code=404, 
            detail="Operação Cancelada: O ID desse Estado inserido não tem registros no banco. Cadastre um Estado correto via POST antes de criar novas Cidades."
        )

    # Continuação natural lógica se a rigorosa checagem superior deu passagem completa
    nova_cidade = models.Cidade(
        nome_cidade=cidade.nome_cidade,
        cod_estado=cidade.cod_estado
    )
    db.add(nova_cidade)
    db.commit()
    db.refresh(nova_cidade)
    return nova_cidade

# Rota para Listar Cidades Amplamente
@app.get("/cidades/", response_model=List[schemas.CidadeResponse])
def listar_cidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lista_cidades = db.query(models.Cidade).offset(skip).limit(limit).all()
    return lista_cidades

# Rota para Buscar Isoladamente Uma Cidade Específica 
@app.get("/cidades/{cod_cidade}", response_model=schemas.CidadeResponse)
def buscar_cidade(cod_cidade: int, db: Session = Depends(get_db)):
    cidade = db.query(models.Cidade).filter(models.Cidade.cod_cidade == cod_cidade).first()
    if cidade is None:
        raise HTTPException(status_code=404, detail="Cidade Inexistente no Banco.")
    return cidade

# Rota de Manutenção e Atualização de Cidades Substitutas
@app.put("/cidades/{cod_cidade}", response_model=schemas.CidadeResponse)
def atualizar_cidade(cod_cidade: int, cidade_nova: schemas.CidadeCreate, db: Session = Depends(get_db)):
    cidade = db.query(models.Cidade).filter(models.Cidade.cod_cidade == cod_cidade).first()
    if cidade is None:
        raise HTTPException(status_code=404, detail="Cidade Não Localizada.")
        
    # Mais checagens obrigatórias relativas a Fantasmas e Alteração Irregular!
    estado_existe = db.query(models.Estado).filter(models.Estado.cod_estado == cidade_nova.cod_estado).first()
    if estado_existe is None:
        raise HTTPException(status_code=404, detail="Operação Irregular Recusada: Novo número de Estado pretendido está sem vínculo válido de cadastramento.")

    cidade.nome_cidade = cidade_nova.nome_cidade
    cidade.cod_estado = cidade_nova.cod_estado
    
    db.commit()
    db.refresh(cidade)
    return cidade

# Rota Varredora para Deletar Cidades
@app.delete("/cidades/{cod_cidade}", status_code=204)
def deletar_cidade(cod_cidade: int, db: Session = Depends(get_db)):
    cidade = db.query(models.Cidade).filter(models.Cidade.cod_cidade == cod_cidade).first()
    if cidade is None:
        raise HTTPException(status_code=404, detail="Cidade Inexistente Restritiva.")
    
    db.delete(cidade)
    db.commit()
    return None
# ==========================================
# ROTAS DA TABELA ALUNOS
# ==========================================

# Rota para Matricular Novo Aluno
@app.post("/alunos/", response_model=schemas.AlunoResponse, status_code=201)
def criar_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    
    # Conferência protetora primária ligando o código cidade
    cidade_existe = db.query(models.Cidade).filter(models.Cidade.cod_cidade == aluno.cod_cidade).first()
    
    if cidade_existe is None:
        raise HTTPException(status_code=404, detail="Matrícula Negada: A cidade relatada não tem código numérico referenciado criado na base.")

    novo_aluno = models.Aluno(**aluno.model_dump())
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

# Rota de Chamada e Listagem Pública de Alunos
@app.get("/alunos/", response_model=List[schemas.AlunoResponse])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Desafio proposto e resolvido: Buscar e entregar visualmente apenas alunos ativos lógicos (True)!
    lista_alunos = db.query(models.Aluno).filter(models.Aluno.ativo_aluno == True).offset(skip).limit(limit).all()
    return lista_alunos

# Atualizar Dados Cadastrais do Aluno
@app.put("/alunos/{cod_aluno}", response_model=schemas.AlunoResponse)
def atualizar_aluno(cod_aluno: int, aluno_novo: schemas.AlunoCreate, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.cod_aluno == cod_aluno).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Perfil Estudantil não registrado e nunca encontrado.")
        
    cidade_existe = db.query(models.Cidade).filter(models.Cidade.cod_cidade == aluno_novo.cod_cidade).first()
    if cidade_existe is None:
        raise HTTPException(status_code=404, detail="Alteração Categórica Recusada: Número referencial de cidade errôneo de preenchimento.")

    aluno.nome_aluno = aluno_novo.nome_aluno
    aluno.email_aluno = aluno_novo.email_aluno
    aluno.idade_aluno = aluno_novo.idade_aluno
    aluno.cod_cidade = aluno_novo.cod_cidade
    aluno.data_cadastro_aluno = aluno_novo.data_cadastro_aluno
    aluno.ativo_aluno = aluno_novo.ativo_aluno
    
    db.commit()
    db.refresh(aluno)
    return aluno

# Rota Famosa de Exclusão Lógica e Soft Delete (Truque de Mercado)
@app.delete("/alunos/{cod_aluno}")
def exclusao_corporativa_aluno(cod_aluno: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.cod_aluno == cod_aluno).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno Alvo inexistente na rede acadêmica consultada.")
    
    # No lugar da remoção forçada permanente do Python na máquina de SQL, realizamos o bloqueio de Status binário!
    aluno.ativo_aluno = False
    db.commit()
    
    return {"informativo_padrao": "O aluno selecionado foi inativado fisicamente com excelente progresso logado no banco relacional MariaDB seguro."}

# ==========================================
# ROTAS DA TABELA CURSOS (Livre de Restrição Estrangeira)
# ==========================================

# Rota Autônoma Base para Lançamento
@app.post("/cursos/", response_model=schemas.CursoResponse, status_code=201)
def criar_curso(curso: schemas.CursoCreate, db: Session = Depends(get_db)):
    novo_curso = models.Curso(**curso.model_dump())
    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)
    return novo_curso

# Listagem Universal Genérica Baseada na Ilimitada Tela
@app.get("/cursos/", response_model=List[schemas.CursoResponse])
def listar_cursos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lista = db.query(models.Curso).offset(skip).limit(limit).all()
    return lista

# Seleção Específica Curricular Baseada Unicamente Pelo Sistema Relacional Fixo ID Numérico Restrito
@app.get("/cursos/{cod_curso}", response_model=schemas.CursoResponse)
def buscar_curso(cod_curso: int, db: Session = Depends(get_db)):
    curso = db.query(models.Curso).filter(models.Curso.cod_curso == cod_curso).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Matriz Restringida Erro: Grade curricular codificada inatingível publicamente e inexistente fisicamente operante em bancos.")
    return curso

# Alinhamento Base e Substituição Cadastral Em Fluxo
@app.put("/cursos/{cod_curso}", response_model=schemas.CursoResponse)
def atualizar_curso(cod_curso: int, curso_novo: schemas.CursoCreate, db: Session = Depends(get_db)):
    curso = db.query(models.Curso).filter(models.Curso.cod_curso == cod_curso).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Manutenção Recusada em Parede Bloqueada: Referência central educacional pretendida encontra-se inatingível e não mapeada localmente.")

    curso.nome_curso = curso_novo.nome_curso
    curso.carga_horaria_curso = curso_novo.carga_horaria_curso
    curso.preco_curso = curso_novo.preco_curso

    db.commit()
    db.refresh(curso)
    return curso

# Extinção Direta Exclusivamente Plena Desvinculada de Cursos Descontinuados da Matriz Unida Prática
@app.delete("/cursos/{cod_curso}", status_code=204)
def deletar_curso(cod_curso: int, db: Session = Depends(get_db)):
    curso = db.query(models.Curso).filter(models.Curso.cod_curso == cod_curso).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Operação Restrita Varredora Negada Plenamente: Nenhum objeto de sistema condizente em código real rastreável isoladamente.")

    db.delete(curso)
    db.commit()
    return None
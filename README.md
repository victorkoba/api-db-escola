# API BD Escola

API REST desenvolvida com FastAPI para gerenciamento de dados escolares.

---

## Tecnologias

* Python
* FastAPI
* AWS Cloud9
* EC2
* MariaDB
* SQLAlchemy

---

## Funcionalidades

* CRUD de alunos
* CRUD de cursos
* CRUD de estados e cidades

---

## Documentação da API

A documentação interativa está disponível em:

- Swagger UI: http://SEU_IP:8000/docs
- ReDoc: http://SEU_IP:8000/redoc

> Observação: a porta pode variar dependendo da configuração do servidor.
## Swagger UI
<img width="1920" height="964" alt="image" src="https://github.com/user-attachments/assets/49d997e2-7459-454b-b5b2-93487116b003" />
## Redoc
<img width="1920" height="968" alt="image" src="https://github.com/user-attachments/assets/09f7d987-92a3-485c-b77d-d0a6109a9fbe" />

## Como rodar o projeto

### 1. Clone o repositório

```
git clone https://github.com/victorkoba/api-db-escola.git
cd api-db-escola
```

---

### 2. Crie e ative o ambiente virtual

```
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instale as dependências

```
pip install -r requirements.txt
```

---

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env`:

```
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nome_do_banco
```

---

### 5. Execute a API

```
python -m uvicorn app.main:app --reload
```

---

## Deploy na AWS (EC2)

A aplicação foi implantada em uma instância EC2 utilizando Uvicorn como servidor ASGI.

### Configuração de rede

No Security Group da instância, foi liberada a porta:

- 8000 (API FastAPI)

---

## Script de configuração do servidor

O projeto inclui um script de automação:

```
scriptexe.sh
```

### O que ele faz:

* Atualiza pacotes do sistema
* Instala Apache, PHP e MariaDB
* Configura permissões do servidor
* Configura o banco de dados automaticamente
* Instala phpMyAdmin

**Atenção:**
As credenciais definidas no script (como senha do usuário root do banco) são apenas para fins de estudo e demonstração.

**Não utilize essas configurações em ambiente de produção.**
O ideal é utilizar variáveis de ambiente e senhas seguras.

### Como executar:

```
chmod +x scriptexe.sh
./scriptexe.sh
```

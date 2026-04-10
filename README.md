# API BD Escola

API de gerenciamento escolar desenvolvida com FastAPI e SQLAlchemy, provisionada em ambiente AWS para demonstração de habilidades em desenvolvimento backend e infraestrutura em nuvem.

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

A API segue o padrão OpenAPI, gerando documentação automática que facilita o consumo dos endpoints e testes em tempo real.

- Swagger UI: http://SEU_IP:8000/docs
- ReDoc: http://SEU_IP:8000/redoc

> Observação: a porta pode variar dependendo da configuração do servidor.

## Swagger UI
<img width="1920" height="964" alt="image" src="https://github.com/user-attachments/assets/49d997e2-7459-454b-b5b2-93487116b003" />

## Redoc
<img width="1920" height="968" alt="image" src="https://github.com/user-attachments/assets/09f7d987-92a3-485c-b77d-d0a6109a9fbe" />

---

## Ambiente de Desenvolvimento
<img width="1920" height="962" alt="image" src="https://github.com/user-attachments/assets/293443b9-2374-4dfc-a7d5-890b8832716a" />

---

## Configuração de rede

No Security Group da instância, foram configuradas as regras de entrada:

- Porta 8000: Tráfego para a API FastAPI.

- Porta 3306: Acesso ao MariaDB (restrito via bind-address e permissões de usuário).

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

## Como rodar
1. Clone o repositório.
2. Configure as variáveis de ambiente em um arquivo `.env` (conforme `.env.example`).
3. Certifique-se de que o MariaDB está rodando (configurado via scriptexe.sh) e o banco api_escola foi criado.
4. Execute `pip install -r requirements.txt`.
5. Inicie com `python -m uvicorn app.main:app --reload`.

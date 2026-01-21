# Edge Monitor API – Backend de Monitoramento, Auditoria e Dashboard

Backend desenvolvido em **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** utilizando **[Django 5.2](https://docs.djangoproject.com/en/5.2/)** e **[Django REST Framework](https://www.django-rest-framework.org/)** para atuar como camada central de **ingestão, persistência, auditoria e visualização** dos eventos de risco detectados por dispositivos **edge**.

Este projeto de **monitoramento de risco em ambientes industriais**, integra-se diretamente ao projeto **Edge Risk Monitor**, responsável pela inferência local com **Visão Computacional**.

A API recebe eventos estruturados e evidências visuais, aplica autenticação segura baseada em JWT, mantém histórico auditável e disponibiliza dados consolidados para dashboards.

---

## Objetivos do Projeto

- Centralizar a ingestão de eventos enviados por dispositivos edge
- Persistir evidências visuais associadas às detecções
- Implementar autenticação segura baseada em JWT
- Disponibilizar fluxo completo de recuperação de senha por e-mail
- Garantir rastreabilidade completa por meio de logs de auditoria
- Disponibilizar dados para visualização analítica (dashboard)
- Documentar a API utilizando OpenAPI / Swagger
- Manter código organizado, legível e aderente a padrões profissionais

---

## Funcionalidades

| Categoria | Descrição |
|----------|-----------|
| **Autenticação JWT** | Login, renovação de token e logout |
| **Recuperação de Senha** | Solicitação de redefinição via e-mail |
| **Redefinição de Senha** | Atualização segura usando UID + token |
| **Gestão de Usuários** | Criação, listagem, edição e exclusão |
| **Ingestão de Eventos Edge** | Recebimento de eventos estruturados |
| **Persistência de Evidências** | Armazenamento de imagens associadas |
| **Dashboard Analítico** | Consulta e filtros por período |
| **Auditoria** | Registro de ações e eventos críticos |
| **Integração Frontend** | API preparada para consumo web |

---

## Tecnologias Utilizadas

## Tecnologias Utilizadas

| Categoria | Tecnologia |
|----------|------------|
| **Linguagem** | **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** |
| **Framework Web** | **[Django 5.2](https://docs.djangoproject.com/en/5.2/)** |
| **API REST** | **[Django REST Framework](https://www.django-rest-framework.org/)** |
| **Autenticação** | **[SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)** |
| **Documentação** | **[drf-spectacular](https://drf-spectacular.readthedocs.io/)** |
| **Banco de Dados** | **[PostgreSQL](https://www.postgresql.org/docs/)** |
| **E-mail (SMTP)** | **[Django Email](https://docs.djangoproject.com/en/5.2/topics/email/)** |
| **Configuração** | **[python-decouple](https://github.com/HBNetwork/python-decouple)**, **[python-dotenv](https://pypi.org/project/python-dotenv/)** |
| **CORS** | **[django-cors-headers](https://github.com/adamchainz/django-cors-headers)** |

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Estrutura de Diretórios

```bash
edge-monitor-api/
├── auth/                             # Autenticação e segurança
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── users/                            # Gestão de usuários
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── monitoring/                       # Eventos de monitoramento
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── dashboard/                        # Dashboard analítico
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── core/                            # Infraestrutura e auditoria
│   ├── models.py                    # LogSystem
│   └── utils.py                     # Função report_log
│
├── media/                            # Evidências (imagens)
│
├── project/
│   ├── settings.py                  # Configurações centrais
│   ├── urls.py                      # Roteamento principal
│   └── wsgi.py
│
├── manage.py
├── .env                             # Variáveis de ambiente
└── README.md
```
---

## Instalação e Execução

### Pré-requisitos

- **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)**
- **[pip](https://pip.pypa.io/en/stable/)**
- **[virtualenv](https://docs.python.org/pt-br/3/library/venv.html)** (opcional, recomendado)
- **[PostgreSQL](https://www.postgresql.org/docs/)** ou outro banco compatível
- **[Git](https://git-scm.com/doc)**
---

### Passo 1 – Clonar o repositório

```bash
$ git clone https://github.com/ruantor4/edge-monitor-api
$ cd edge-monitor-api
```

### Passo 2 – Criar ambiente virtual
```bash
$ python -m venv .dev
$ source .dev/bin/activate        # Linux / macOS
# .dev\Scripts\activate           # Windows
```
### Passo 3 – Instalar dependências
```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
``` 
### Passo 4 – Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
SECRET_KEY=chave-secreta-do-django
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=monitor_api
DB_USER=admin
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
```

### Passo 5 – Aplicar migrações do banco de dados
```bash
$ python manage.py makemigrations
$ python manage.py migrate
``` 
### Passo 6 – Criar usuário administrador
```bash
$ python manage.py createsuperuser
```

### Passo 7 – Executar o servidor de desenvolvimento
```bash
$ python manage.py runserver
``` 

---

## Documentação da API (Swagger)

A documentação OpenAPI é gerada automaticamente.

- Swagger UI
```bash
    http://127.0.0.1:8000/
```
- Schema OpenAPI
```bash
    http://127.0.0.1:8000/api/schema/
```
---

## Auditoria e Logs

- Todas as ações críticas são auditadas
- Tokens JWT com expiração configurável
- Recuperação de senha sem enumeração de usuários
- Frontend nunca recebe informações sensíveis

---

## Integração com o Edge Risk Monitor

- **Edge Risk Monitor** → inferência em borda
- **Edge Monitor API** → persistência, auditoria e análise
- **Edge Monitor Frontend** → interface web

Arquitetura desacoplada, orientada a eventos e escalável.

---

## Observações Técnicas

O backend foi projetado com foco em:

- Segurança
- Clareza arquitetural
- Auditoria
- Escalabilidade
- Integração industrial real
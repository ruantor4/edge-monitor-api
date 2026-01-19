# Edge Monitor API – Backend de Monitoramento, Auditoria e Dashboard

Backend desenvolvido em **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** utilizando **[Django 5.2](https://docs.djangoproject.com/en/5.2/)** e **[Django REST Framework](https://www.django-rest-framework.org/)** para atuar como camada central de **ingestão, persistência, auditoria e visualização** dos eventos de risco detectados por dispositivos **edge**.

Este projeto de **monitoramento de risco em ambientes industriais**, integra-se diretamente ao projeto **Edge Risk Monitor**, responsável pela inferência local com **Visão Computacional**.

A API recebe eventos estruturados e evidências visuais, aplica regras de autenticação, mantém histórico auditável e disponibiliza dados consolidados para dashboards.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Objetivos do Projeto

- Centralizar a ingestão de eventos de monitoramento enviados por dispositivos edge
- Persistir evidências visuais associadas às detecções
- Implementar autenticação segura baseada em JWT
- Garantir rastreabilidade completa por meio de logs de auditoria
- Disponibilizar dados para visualização analítica (dashboard)
- Documentar a API utilizando OpenAPI / Swagger
- Manter código organizado, legível e aderente a padrões profissionais

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Funcionalidades

| Categoria | Descrição |
|----------|-----------|
| **Autenticação JWT** | Autenticação segura baseada em tokens, com suporte a login, renovação e logout |
| **Gestão de Usuários** | Criação, listagem, consulta, atualização e exclusão de usuários do sistema |
| **Ingestão de Eventos de Monitoramento** | Recebimento de eventos estruturados enviados por dispositivos edge |
| **Persistência de Evidências** | Armazenamento de evidências visuais associadas aos eventos de detecção |
| **Dashboard Analítico** | Consulta e visualização de eventos filtrados por intervalo de datas |
| **Auditoria e Rastreabilidade** | Registro estruturado de ações, operações e eventos do sistema |
| **Integração com Sistemas Edge** | Backend preparado para integração direta com aplicações de inferência em borda |


**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Tecnologias Utilizadas

| Categoria | Tecnologia |
|----------|------------|
| **Linguagem** | **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** |
| **Framework Web** | **[Django 5.2](https://docs.djangoproject.com/en/5.2/)** |
| **API REST** | **[Django REST Framework](https://www.django-rest-framework.org/)** |
| **Autenticação** | **[SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)** |
| **Documentação API** | **[drf-spectacular](https://drf-spectacular.readthedocs.io/)** |
| **Banco de Dados** | **[PostgreSQL](https://www.postgresql.org/docs/)** |
| **Uploads de Arquivos** | **[Django Media Files](https://docs.djangoproject.com/en/5.2/topics/files/)** |
| **Configuração** | **[python-decouple](https://github.com/HBNetwork/python-decouple)**, **[python-dotenv](https://pypi.org/project/python-dotenv/)** |

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Estrutura de Diretórios

```bash
edge-monitor-api/
├── auth/                             # Autenticação e tokens JWT
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
├── core/                             # Infraestrutura e auditoria
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

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

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

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

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
**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Auditoria e Logs

O sistema mantém auditoria completa de ações e eventos relevantes,
garantindo rastreabilidade, análise histórica e suporte à investigação
de falhas operacionais.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Integração com o Edge Risk Monitor

Este backend foi projetado para integração direta com o projeto **Edge Risk Monitor**,
responsável pela inferência local com **YOLO** e envio apenas de eventos confirmados.

Essa integração permite:
- Processamento pesado realizado na borda (edge)
- Backend dedicado à persistência, auditoria e visualização
- Arquitetura desacoplada, escalável e orientada a eventos

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Observações Técnicas

A solução segue princípios de separação de responsabilidades,
com inferência restrita ao edge e backend focado em persistência,
auditoria e análise, respeitando padrões REST e boas práticas
de organização de código.

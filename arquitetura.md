## 1. Visão geral do Sistema B (edge-monitor-api)

### Missão do sistema

Atuar como API central para autenticação, gestão de usuários e armazenamento/consulta de ocorrências de risco detectadas pelo Sistema A.

#### O que o sistema FAZ

- Autentica usuários (JWT)

- Recebe eventos de detecção

- Armazena evidências

- Fornece dados para dashboard

#### O que o sistema NÃO FAZ

- Inferência

- Processamento de imagem

- Stream de vídeo

- Regras de negócio complexas

2. Arquitetura lógica (apps e responsabilidades)
```bash
    edge-monitor-api/
├── manage.py
├── requirements.txt
│
├── project/                        # Configuração global do Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Django + DRF + JWT + PostgreSQL
│   ├── urls.py                     # Roteamento central da API
│   └── wsgi.py
│
├── users/                          # Fase 2 — Usuários
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── serializers.py              # User serializers (CRUD)
│   ├── views.py                    # Endpoints /api/user/
│   ├── urls.py                     # Rotas de usuário
│   └── tests.py
│
├── monitoring/                     # Fase 4 — Monitoramento
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # MonitoringEvent
│   ├── serializers.py              # Serializer da ocorrência
│   ├── views.py                    # /api/monitoring/ e /api/dashboard
│   ├── urls.py                     # Rotas de monitoramento
│   ├── migrations/
│   │   └── __init__.py
│   └── tests.py
│
├── media/                          # Upload de evidências (runtime)
│   └── evidence/
│
└── .env                            # Variáveis de ambiente (não versionar)
```
## 3. Padrões técnicos adotados (imutáveis)

#### 3.1 Frameworks

- Django

- Django REST Framework

- SimpleJWT

- PostgreSQL

#### 3.2 Autenticação

- JWT Bearer Token

- Access token curto

- Refresh token longo

- Logout por blacklist

#### 3.3 Estilo de API

- REST

- JSON

- Status HTTP corretos

- Nomes de endpoints conforme edital

## 4. Contrato da API (definitivo)

#### 4.1 Autenticação
Login:
```bash
POST /api/autentication/login/
``` 

Request:
```bash
{
  "username": "user",
  "password": "senha"
}
``` 

Response:
```bash
{
  "token_access": "...",
  "token_renovation": "..."
}
``` 
Renovar token
```bash
POST /api/autentication/renovate/
``` 
Logout
```bash
POST /api/autentication/logout/
```

#### 4.2 Usuários
```bash
POST   /api/user/
GET    /api/user/
GET    /api/user/{id}/
PUT    /api/user/{id}/
DELETE /api/user/{id}/
```
Campos:

- username

- email

- password

#### 4.3 Monitoramento
```bash
POST /api/monitoring/
```
Headers:
```bash
Authorization: Bearer <access_token>
```
Body (multipart/form-data):

- MAC

- DATE

- CLASS

- EVIDENCE

#### 4.4 Dashboard
```bash
GET /api/dashboard?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

Response:
```bash
[
  {
    "mac": "...",
    "class": "mouse",
    "datetime": "...",
    "image": "url"
  }
]
```

## 5. Padrões de código
#### 5.1 Serializers

- 1 serializer por endpoint principal

- Validação explícita

- Sem lógica pesada

#### 5.2 Views

- Class-based views (DRF)

- Cada endpoint isolado

- Permissões declarativas

#### 5.3 Models

- Apenas dados

- Nada de regra de negócio

## 6. Ordem de implementação (checklist)
#### Fase 1 — Base

- Django

- DRF

- JWT

- PostgreSQL

#### Fase 2 — Usuários

- App users

- Serializer

- CRUD

#### Fase 3 — Autenticação

- Login

- Refresh

- Logout

#### Fase 4 — Monitoramento

- App monitoring

- Model

- Upload de imagem

#### Fase 5 — Dashboard

- Filtro por data
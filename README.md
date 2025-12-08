# RNJ-Connect

Plataforma de Gamificación para la Red Nacional de Jóvenes Scouts

## 🏗️ Arquitectura del Proyecto

```
RNJ-Connect/
├── backend/                    # API Python FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints API
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── chat.py
│   │   │   │   │   └── gamification.py
│   │   │   │   └── api.py
│   │   │   └── deps.py
│   │   ├── core/              # Configuración central
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── websocket.py
│   │   ├── models/            # Modelos SQLModel/SQLAlchemy
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   └── gamification.py
│   │   ├── schemas/           # Schemas Pydantic
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   └── gamification.py
│   │   ├── services/          # Lógica de negocio
│   │   │   ├── user_service.py
│   │   │   ├── chat_service.py
│   │   │   └── gamification_service.py
│   │   ├── database.py        # Configuración DB
│   │   └── main.py            # Punto de entrada
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/                   # App Vue 3
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   │   └── styles/
│   │   │       └── main.css
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── auth/
│   │   │   ├── chat/
│   │   │   └── gamification/
│   │   ├── composables/
│   │   ├── layouts/
│   │   │   └── DefaultLayout.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── stores/
│   │   │   ├── auth.js
│   │   │   ├── user.js
│   │   │   └── chat.js
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   └── Dashboard.vue
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── websocket.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.js
│
└── .gitignore
```

## 🚀 Stack Técnico

### Backend
- **FastAPI** (Python 3.11+)
- **SQLModel** / **SQLAlchemy** (ORM)
- **SQL Server** (Base de datos)
- **Pydantic** (Validación de datos)
- **WebSockets** (Chat en tiempo real)
- **JWT** (Autenticación)

### Frontend
- **Vue 3** (Composition API con `<script setup>`)
- **Vite** (Build tool)
- **Pinia** (State management)
- **Vue Router** (Routing)
- **TailwindCSS** (Estilos)
- **Axios** (HTTP client)

## 📦 Instalación

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend

```powershell
cd frontend
npm install
```

## ⚙️ Configuración

### Backend (.env)

```env
# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database
DATABASE_URL=mssql+pyodbc://user:password@localhost:1433/rnjconnect?driver=ODBC+Driver+17+for+SQL+Server

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 🏃 Ejecutar el Proyecto

### Backend

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```powershell
cd frontend
npm run dev
```

## 📚 Endpoints Principales

- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

## 🧪 Testing

```powershell
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 📄 Licencia

Proyecto interno - Red Nacional de Jóvenes Scouts

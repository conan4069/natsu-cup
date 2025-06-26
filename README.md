# 🛠 Proyecto Fullstack: Django + Vue 3 + Docker

Este proyecto combina **Django (backend)** y **Vue 3 (frontend)** dentro de una única estructura, usando **Docker** para facilitar el desarrollo. Si estás empezando, no te preocupes: aquí tienes todo paso a paso 🚀

---

## 📁 Estructura del proyecto

. ├── core/ # Proyecto Django (settings.py, wsgi, etc.) 
  ├── apps/ # Aplicaciones del backend 
  ├── frontend/ # Proyecto Vue 3 (con Router, Pinia, Tailwind) 
  ├── manage.py # Entrada de Django 
  ├── requirements.txt # Dependencias del backend 
  ├── Dockerfile # Backend 
  ├── docker-compose.yml # Orquestador de servicios 
  
---

## ✅ Requisitos

- Tener instalado:
  - [Docker](https://www.docker.com/)
  - [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) Git para clonar el repo

---

## ⚙️ Configuración rápida

### 1. Clona el repositorio

```bash
git clone https://github.com/conan4069/natsu-cup.git
cd natsu-cup
```

## Levantar el proyecto

```bash
docker-compose up --build
```

## Cuando haya un cambio en los modelos
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
---

## 🌐 Accesos rápidos
Frontend (Vue 3): http://localhost:5173

Backend (API Django): http://localhost:8000

Admin Django: http://localhost:8000/admin

---
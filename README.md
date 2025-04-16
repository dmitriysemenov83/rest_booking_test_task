# 🪑 R-Booking — Сервис бронирования столиков

R-Booking — это REST API для управления бронированием столиков в ресторане.  
Проект реализован с использованием **FastAPI**, **PostgreSQL**, **SQLAlchemy** и запускается через **Docker Compose**.

---

## 🚀 Быстрый старт

- Docker
- Docker Compose

### 📁 Клонируем репозиторий

```bash
git clone https://github.com/dmitriysemenov83/rest_booking_test_task
cd r-booking
```
## 🐳 Запуск в Docker

```bash
docker-compose build
docker-compose up
```
После запуска:

- API будет доступен по адресу: http://localhost:8000

- Swagger-документация: http://localhost:8000/docs

## 🛠 Стек технологий

- FastAPI — веб-фреймворк

- PostgreSQL — база данных

- SQLAlchemy + asyncpg — асинхронный ORM

- Alembic — миграции

- Docker / Docker Compose — контейнеризация

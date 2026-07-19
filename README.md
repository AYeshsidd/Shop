# Coffee Shop Backend — Progress Log

**Stack:** FastAPI + SQLAlchemy + MySQL + JWT (bcrypt for hashing)
**Architecture:** Microservices, feature-by-feature (vertical slices)

## ✅ Completed: Auth Feature

- **Folder structure:** `core/` (shared: db, config, security) + `auth/` (models, schemas, routes, dependencies)
- **DB:** `users` table (MySQL) — id, name, email, password_hash, role (enum: admin/customer), phone, address, timestamps
- **Password security:** bcrypt hashing (direct `bcrypt` lib, not passlib — passlib is unmaintained and broke on newer bcrypt versions)
- **JWT strategy:** access token (30 min) + refresh token (7 days), both signed with `SECRET_KEY` from `.env`
- **Endpoints built:**
  - `POST /auth/register` — creates user, hashes password
  - `POST /auth/login` — verifies password, returns access + refresh token pair
  - `GET /auth/me` — protected route, returns current user (tests token verification via `HTTPBearer`)
  - `POST /auth/refresh` — exchanges valid refresh token for new access + refresh token pair
- **Role handling:** role comes only from DB (never trusted from login input); role input is normalized to lowercase via Pydantic validator

## ✅ Migrations: Alembic set up

- Tracks schema changes going forward (no more manual `ALTER`/`DROP TABLE`)
- `alembic/env.py` wired to `.env` DB URL and `Base.metadata`
- First migration applied: synced `users` table, dropped unused legacy `products` table

## ⏳ Next steps

- Role-based route protection (admin-only actions)
- Frontend: full auth flow (login form, token storage, auto-refresh)
- Then: Catalog Service (Categories + Products) — next backend feature

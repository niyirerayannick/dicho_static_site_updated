# DICHO Ltd | Home of ALVI Natural Products

DICHO Ltd is a Django-powered catalogue and ordering website for ALVI natural products. The current Bootstrap frontend, database-driven shop, cart, checkout, forms, and administration are retained.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# For local Windows development, remove SQLITE_PATH and MEDIA_ROOT from .env.
python manage.py migrate
python manage.py runserver
```

The website is available at `http://127.0.0.1:8000/`; Django admin is at `http://127.0.0.1:8000/admin/`.

## Coolify deployment with persistent SQLite

This deployment uses one application container and SQLite. Do not configure replicas or multiple application services while SQLite is in use.

1. Create a GitHub repository and push the project. Commit `initial_db.sqlite3` only if you want the current local database to initialize the first production deployment.
2. In Coolify, create a project and add a new resource from GitHub.
3. Choose **Dockerfile** deployment. Coolify builds the included `Dockerfile` and starts `entrypoint.sh`.
4. Set these environment variables in Coolify:

   ```text
   SECRET_KEY=<a-long-random-secret>
   DEBUG=False
   ALLOWED_HOSTS=dicho.rw,www.dicho.rw
   CSRF_TRUSTED_ORIGINS=https://dicho.rw,https://www.dicho.rw
   SQLITE_PATH=/app/data/db.sqlite3
   MEDIA_ROOT=/app/media
   ```

5. Add persistent storage mounts in Coolify:

   ```text
   /app/data   # persistent SQLite directory
   /app/media  # persistent uploaded media directory
   ```

6. Deploy. On the first deployment only, `entrypoint.sh` copies `/app/initial_db.sqlite3` into `/app/data/db.sqlite3` when the persistent database does not already exist. It also copies `/app/initial_media` into an empty `/app/media` volume when that optional bootstrap directory exists.
7. Create an administrator from the Coolify terminal:

   ```sh
   python manage.py createsuperuser
   ```

8. Confirm the admin at `/admin/`.

Future GitHub deployments update code, migrations, and static files. They do **not** overwrite `/app/data/db.sqlite3` or `/app/media`, because those paths are persistent Coolify storage mounts and the bootstrap copies run only when those destinations are empty.

### Initial data and media

`initial_db.sqlite3` is first-deployment-only data, not the live production database. The project ignores `db.sqlite3` and `media/`, while intentionally allowing optional `initial_db.sqlite3` and `initial_media/` to be committed. If the database or images contain private data, do not commit those bootstrap files; upload them to the corresponding Coolify persistent storage instead before the first deployment.

## Backups

GitHub stores code, not the live production data. Before a major deployment and regularly thereafter:

1. Download or copy `/app/data/db.sqlite3` from the persistent storage.
2. Download or copy `/app/media` as well.
3. Keep both together, because the database records reference the uploaded files in the media directory.

## Local production-style checks

```powershell
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
docker build -t dicho .
docker run -p 8000:8000 `
  -e SECRET_KEY=test-secret-key `
  -e DEBUG=False `
  -e ALLOWED_HOSTS=localhost,127.0.0.1 `
  -e CSRF_TRUSTED_ORIGINS=http://localhost:8000 `
  -e SQLITE_PATH=/app/data/db.sqlite3 `
  -e MEDIA_ROOT=/app/media `
  -v dicho_sqlite_data:/app/data `
  -v dicho_media:/app/media `
  dicho
```

Open `http://127.0.0.1:8000/` after the container starts.

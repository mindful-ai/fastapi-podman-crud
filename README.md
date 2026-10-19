# FastAPI Podman CRUD Demo

A minimal FastAPI product CRUD API with pytest tests and a Podman-compatible Containerfile.

## Project files

- `main.py` — FastAPI CRUD endpoints and `/health`
- `test_main.py` — 11 automated tests
- `requirements.txt` — runtime dependencies
- `requirements-dev.txt` — runtime dependencies plus pytest/httpx
- `Containerfile` — builds the production application image
- `.containerignore` — excludes local/test files from the image build context

## 1. Run locally (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -v
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/docs>.

## 2. Build and run with Podman

```bash
podman --version
podman build -t fastapi-podman-crud:1.0 .
podman run -d --name fastapi-crud -p 8000:8000 fastapi-podman-crud:1.0
podman ps
podman logs fastapi-crud
```

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Open <http://localhost:8000/docs> to exercise the CRUD endpoints.

## 3. Example CRUD requests (Bash)

Create:

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"LED TV","price":24999,"quantity":10}'
```

List:

```bash
curl http://localhost:8000/products
```

Read one:

```bash
curl http://localhost:8000/products/1
```

Update:

```bash
curl -X PUT http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"LED TV 43 inch","price":27999,"quantity":8}'
```

Delete:

```bash
curl -X DELETE http://localhost:8000/products/1
```

## Notes

- This is a learning starter project. Product records are stored in memory and are lost when the application process/container is recreated.
- The container image includes only runtime dependencies; run pytest on the host for now.
- If host port 8000 is busy, publish a different host port, e.g. `-p 8001:8000`.

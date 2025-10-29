## cram-backend

Minimal Django backend for the cram MVP. It exposes a REST API for fetching languages, situations, prompts, and communications filtered by learner language preferences.

### Prerequisites

- Python 3.12 or newer
- Poetry for dependency management

Install dependencies and apply migrations:

```bash
poetry install
poetry run python manage.py migrate
```

Start the development server:

```bash
poetry run python manage.py runserver
```

### API quickstart

Full endpoint documentation lives in `API.md`. The commands below hit the core endpoints once the server is running at `http://localhost:8000`.

All situation, prompt, communication, and context payloads now expose a single `description` string rather than language-specific description collections.

List all languages:

```bash
curl http://localhost:8000/api/languages/
```

List situations for a specific language (example: English `eng`):

```bash
curl http://localhost:8000/api/languages/deu/situations/
```

Fetch the full situation bundle:

```bash
curl "http://localhost:8000/api/situations/3/?target_lang=deu&native_lang=eng"
```

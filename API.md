# API Reference

All endpoints are served under the `/api/` prefix and return JSON. Unless otherwise stated, responses use HTTP status `200 OK` on success. Error responses follow Django REST framework’s default error envelope:

```json
{"detail": "<human-readable message>"}
```

Date/time fields are rendered as ISO-8601 strings in UTC (e.g. `"2025-10-28T17:42:13.123456Z"`).

## Authentication

No authentication is required for these endpoints in the current MVP.

## Endpoints

### 1. List all languages

- **Method**: `GET`
- **URL**: `/api/languages/`

#### Response

```json
[
  {
    "id": 1,
    "code": "eng",
    "name": "English"
  },
  {
    "id": 2,
    "code": "spa",
    "name": "Spanish"
  }
]
```

### 2. List situations for a given language

- **Method**: `GET`
- **URL**: `/api/languages/{language_code}/situations/`
  - `language_code`: ISO-639 code that matches `Language.code`.

#### Response

Each situation includes the shared `description` text for the scenario.

```json
[
  {
    "id": 12,
    "last_updated": "2025-10-28T17:35:54.971538Z",
    "image_url": "https://cdn.example/situation-12.jpg",
    "language_code": "eng",
    "description": "Meeting someone for the first time."
  }
]
```

### 3. Situation bundle (filtered by language pair)

- **Method**: `GET`
- **URL**: `/api/situations/{situation_id}/`
  - `situation_id`: numeric `Situation` primary key.
- **Required query parameters**:
  - `target_lang`: ISO-639 code (must match `Language.code`) representing the learner’s *target* language.
  - `native_lang`: ISO-639 code representing the learner’s *native* language.

If either query parameter is missing, the API returns `400` with an explanatory message.

#### Response

The payload aggregates all content relevant to the situation for the provided language pair:

```json
{
  "situation": {
    "id": 12,
    "last_updated": "2025-10-28T17:35:54.971538Z",
    "image_url": "https://cdn.example/situation-12.jpg",
    "language": "eng",
    "description": "Meeting someone for the first time."
  },
  "prompts": [
    {
      "id": 7,
      "last_updated": "2025-10-28T17:35:54.971538Z",
      "description": "Greet a new acquaintance politely."
    }
  ],
  "communications": [
    {
      "id": 30,
      "last_updated": "2025-10-28T17:35:54.971538Z",
      "shouldBeExpressed": true,
      "shouldBeUnderstood": false,
      "description": "Small talk opener.",
      "utterances": [
        {
          "id": 111,
          "last_updated": "2025-10-28T17:35:54.971538Z",
          "language": "spa",
          "transliteration": "o-la",
          "content": "Hola, ¿cómo estás?",
          "contexts": [
            {
              "id": 501,
              "context_type": "politeness",
              "context_type_details": {
                "id": 4,
                "name": "politeness",
                "description": "Used in polite contexts."
              },
              "description": "Suitable for informal greetings."
            }
          ]
        }
      ]
    }
  ]
}
```

Rules applied:

- `situation.language` in the response echoes the `native_lang` query parameter for backward compatibility.
- Descriptions are no longer language-specific; the same text is returned regardless of the requested `native_lang`.
- `communications` are included only if they reference at least one `Utterance` in `target_lang`.
- Each `communication.utterances` array contains only the `target_lang` utterances.
- `context_type_details` is populated when a `ContextType` exists with `name` matching the context’s `context_type`. Its `description` mirrors the stored context-type text. When no match exists, the field is `null`.

#### Error responses

- `404 Not Found` if the situation id does not exist.
- `404 Not Found` if the situation has no communications with utterances in the requested `target_lang`.
- `400 Bad Request` if `target_lang` or `native_lang` is missing.

## Setup Notes

This project depends on Django REST framework. After updating dependencies (`pyproject.toml`), install them locally:

```bash
poetry install
```

Run migrations as usual:

```bash
poetry run python manage.py migrate
```

## Example Usage

```bash
# Fetch all languages
curl http://localhost:8000/api/languages/

# Fetch situations for English learners
curl http://localhost:8000/api/languages/eng/situations/

# Fetch the localized bundle for situation 12, target Spanish, native English
curl "http://localhost:8000/api/situations/12/?target_lang=spa&native_lang=eng"
```

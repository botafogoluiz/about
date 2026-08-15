# about.luizsilva.fyi

Luiz Silva's personal resume/portfolio site — a Django app that consolidates
his professional experience, blog, and project portfolio in one place for
recruiters, business owners, and anyone curious about his work.

## Features

- **Scrollytelling timeline** — work experience and education rendered as a
  full-viewport, cross-fading background story on the homepage.
- **Blog** — posts with categories/tags and a rich text editor
  ([CKEditor 5](https://ckeditor.com/ckeditor-5/)).
- **Portfolio** — a simple project card grid.
- **Bilingual** — every page is available in English and Brazilian
  Portuguese ([django-modeltranslation](https://github.com/deschler/django-modeltranslation)),
  with a language switcher and locale-prefixed URLs (`/en/...`, `/pt-br/...`).
- **AI-assisted admin** — a "Translate" button in the Django admin uses
  Claude to machine-translate freshly written Portuguese content into
  English (title, body, rich text included), so content only has to be
  written once. Nothing is ever invented — it only translates what's
  already been written.

## Tech stack

- Python / [Django](https://www.djangoproject.com/) 5.x
- PostgreSQL + Redis
- [django-modeltranslation](https://github.com/deschler/django-modeltranslation) for bilingual content
- [django-ckeditor-5](https://github.com/hvlads/django-ckeditor-5) for rich text
- [Anthropic Claude API](https://www.anthropic.com/) for the admin translate feature
- Gunicorn + WhiteNoise, deployed via Docker Compose behind a reverse proxy

## Running locally

```bash
cp .env.example .env   # fill in SECRET_KEY, DB credentials, etc.
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

The site expects a few environment variables (see `config/settings.py`):
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DB_NAME`/`DB_USER`/`DB_PASSWORD`,
and `ANTHROPIC_API_KEY` if you want the admin translate button to work.

## Project structure

- `core/` — shared base template, nav/footer, and the reusable admin
  translate-button mixin (`core/admin_mixins.py`)
- `timeline/` — Experience, Education, Evidence, and Profile models behind
  the homepage
- `blog/` — Post, Category, Tag
- `portfolio/` — Project

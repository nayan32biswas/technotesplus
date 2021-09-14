`docker-compose build api`
`docker-compose up api worker`

Env file

```
API_BROWSER_HOST=http://localhost:8000
SECRET_KEY=ksjrf73y4ner9u2nehf23y74rt784rh
POSTGRES_USER=tech_note_user
POSTGRES_PASSWORD=tech_note_pass
POSTGRES_DB=tech_note
DJANGO_SETTINGS_MODULE=tech_note.development
SENDGRID_API_KEY=SENDGRID_API_KEY
SENDER_EMAIL=example@email.com
```

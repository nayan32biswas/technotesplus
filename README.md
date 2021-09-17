### Note

Make sure you have installed `docker`, `node` and `yarn` on your computer.

### To Start the project run following command
- Navigate to the project directory.
- `docker-compose build api` First build the docker image.
- `docker-compose up api worker` Start backend server.
- `docker-compose run --rm api coverage run manage.py test --noinput` Run tests for backend server
- `docker-compose run --rm api coverage report -m --skip-covered` Get test report.
- `docker-compose run --rm api python manage.py createsuperuser` Create Superuser to access the admin panel.
- `docker-compose run --rm api python manage.py populatedb` Populate database with dumy data.
- Open another terminal and navinate to the frontend directory.
- `yarn install`
- `VUE_APP_DEVHOST=http://localhost:8000 yarn build`

### Demo .env file
```
API_BROWSER_HOST=http://localhost:8000
SECRET_KEY=ksjrf73y4ner9u2nehf23y74rt784rh
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
DJANGO_SETTINGS_MODULE=tech_note.development
SENDGRID_API_KEY=<YUOR SENDGRID_API_KEY>
SENDER_EMAIL=example@email.com
```

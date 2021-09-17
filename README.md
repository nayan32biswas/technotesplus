## Clone project
- `git clone https://github.com/nayan32biswas/technotesplus.git`

### Note

Make sure you have installed `docker`, `node` and `yarn` on your computer.

### To Start the project run follow then instruction.
- Navigate to the project directory.
- Create .env file and assign value
```
API_BROWSER_HOST=http://localhost:8000
SECRET_KEY=ksjrf73y4ner9u2nehf23y74rt784rh
DJANGO_SETTINGS_MODULE=tech_note.development
SENDGRID_API_KEY=<YUOR SENDGRID_API_KEY>
SENDER_EMAIL=example@email.com
```
- Execute `start-project.sh` is sh was supported.
- `docker-compose build api` First build the docker image.
- `docker-compose up api worker` Start backend server.
- `docker-compose run --rm api coverage run manage.py test --noinput` Run tests for backend server
- `docker-compose run --rm api coverage report -m --skip-covered` Get test report.
- `docker-compose run --rm api python manage.py createsuperuser` Create Superuser to access the admin panel.
- `docker-compose run --rm api python manage.py populatedb` Populate database with dummy data.
- Open another terminal and navigate to the frontend directory.
- `yarn install`
- `VUE_APP_DEVHOST=http://localhost:8000 yarn serve`

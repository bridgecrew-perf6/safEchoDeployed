# safEcho


Create an .env file in root directory and place following lines in it

        DATABASE_URL=place database url here # example url postgres://postgres:1234@db:5432/safecho

# Local setup without docker (Manual setup)

install python 3.8

    https://www.python.org/downloads/release/python-380/

install virtaulenv

    https://pypi.org/project/virtualenv/

install redis server for celery

    We are using celery for the periodic tasks(Like curently we are sending invoices on every first of month)
    https://flaviocopes.com/redis-installation/

install postgresql (its the database that we are using ini the project)

    https://www.postgresql.org/download/
    once the installation is done open pgadmin4 and create a database and hit enter

Create virtualenv and activate it open the project in virtaulenv and run command in terminal

    pip install -r requirements.txt

once the installation is finished

    run command
    python manage.py makemigrations
    python manage.py migrate
    python manage.py djstripe_sync_plans_from_stripe
    python manage.py runserver

Now we are moving to run the celery for periodic tasks

    open the terminal and run commmand
    redis-server
    open another terminal and run the following commmand
    celery -A Project worker -B -l info

Done 

# Local setup with docker

Install Docker Compose

    https://docs.docker.com/compose/install/    

Setting up Project with docker

    https://docs.docker.com/compose/django/

Running system with Docker

    docker-compose up -d --build --remove-orphans
    docker-compose exec web python manage.py migrate --noinput # Run mingrations
    
Down docket with volume removed
    
    docker-compose down -v
    docker-compose down #down without removing volumes

Down Docker image

    docker-compose down

Creating super user

    docker-compose exec web python manage.py createsuperuser 

Running commands in docket ENV

    docker-compose exec web python manage.py migrate --noinput

Get and Update Products/Packages from Stripe

    docker-compose exec web python manage.py djstripe_sync_plans_from_stripe
    

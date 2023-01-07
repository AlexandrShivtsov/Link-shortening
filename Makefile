SHELL := /bin/bash

manage_py := python3 app/manage.py

runserver:
	$(manage_py) runserver

worker:
	cd app && celery -A app worker -l info --autoscale=2,1
	#cd app && celery -A app worker -l info --concurrency 10

beat:
	cd app && celery -A app beat -l info

shell:
	$(manage_py) shell

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate
    	
# sudo /etc/init.d/redis-server start
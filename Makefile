all: build down up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

psql:
	docker exec -it jwt_auth__db psql -U postgres

dev:
	docker-compose run --rm --volume=${PWD}/src:/src --publish 8000:8000 app bash -c 'uvicorn app.internal.main:app --host 0.0.0.0 --port 8000 --reload'

# $m [marks]
# $k [keyword expressions]
# $o [other params in pytest notation]
dev_test:
	docker-compose run --volume=${PWD}/src:/src --rm app pytest $(if $m, -m $m)  $(if $k, -k $k) $o

poetry_lock:
	docker-compose run --rm --no-deps --volume=${PWD}:${PWD} --workdir=${PWD} app poetry lock --no-update
	sudo chown -R ${USER} ./poetry.lock

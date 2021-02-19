## pipenv setup
ensure pipenv is installed
```
pip install pipenv --user
```

install dependencies
```
pipenv sync
```

run flask
```
pipenv run python main.py
```

run tests
```
pipenv run python -m pytest
```

## DB setup

create docker network
```
docker network create pg-net
```

init PostgreSQL as docker
```
docker run --network=pg-net -p 5432:5432  --name postgresdb -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=admin -d postgres
```

start Pgadmin as docker
```
docker run --network=pg-net -p 5050:80  -e "PGADMIN_DEFAULT_EMAIL=admin@admin.ch" -e "PGADMIN_DEFAULT_PASSWORD=admin"  -d dpage/pgadmin4
```


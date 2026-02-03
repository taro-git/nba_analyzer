# nba_analizer
This application analyzes NBA players and teams based on box scores and play-by-play data.
# OSS
* client: React Router (Framework)  
* api server: FastAPI   
* batch server: apscheduler 
* database: PostgreSQL  
* CDC (Change Data Capture): Debezium, Kafka 
# Build
### for prod
1. Run following commands
    ```ps
    docker compose --profile prod up --build -d
    ```
### for dev
* docker
  1. Run following commands (Run same commands to rebuild client)
      ```ps
      docker compose --profile dev up --build -d
      ```
* local
  1. Run following commands for client  
      ```ps
      cd client
      npm run install
      npm run dev
      ```
  1. Run following commands for rest api server  
      ```ps
      cd server
      poetry install
      poetry run uvicorn rest_api.main:app --reload
      ```
  1. Run following commands for batch server  
      ```ps
      poetry run uvicorn batch.main:app --reload
      ```
# DB Migration
### for dev
1. Build dev(docker)
1. Update SQLModel
1. Import all models in server\src\common\alembic\env.py
1. Run following commands
    ```ps
    # generate migration file
    docker compose exec app-dev poetry run alembic -c src/common/alembic.ini revision --autogenerate
    # apply db
    docker compose exec app-dev poetry run alembic -c src/common/alembic.ini upgrade head
    ```
### for prod
1. Build prod
1. Run following commands
    ```ps
    # apply db
    docker compose exec app-prod poetry run alembic -c /app/server/src/common/alembic.ini upgrade head
    ```
# lint, test
* client  
    ```ps
    cd client
    # linting
    npm run lint
    npm run format
    # testing
    npm run test
    ```
* server  
    ```ps
    cd server
    # linting
    poetry run ruff format .
    poetry run ruff check . --fix
    # testing
    poetry run pytest
    ```


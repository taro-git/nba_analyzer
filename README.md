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
* server and db
  1. Run following commands (Run same commands to rebuild client)
      ```ps
      docker compose --profile dev up --build -d
      ```
* client
  1. Run following commands for client  
      ```ps
      cd client
      npm run install
      npm run dev
      ```
  1. Access http://localhost:5173/view/ in web browser  
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
    * for downgrade
      ```ps
      docker compose exec app-dev poetry run alembic -c src/common/alembic.ini downgrade base
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


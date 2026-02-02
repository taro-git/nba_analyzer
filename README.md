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
    ```sh
    docker compose --profile prod up --build -d
    ```

### for dev
* docker
  1. Run following commands (Run same commands to rebuild client)
      ```sh
      docker compose --profile dev up --build -d
      ```
* local
  1. Run following commands for client  
      ```sh
      cd client
      npm run install
      npm run dev
      ```
  1. Run following commands for rest api server  
      ```sh
      cd server
      poetry install
      poetry run uvicorn rest_api.main:app --reload
      ```
  1. Run following commands for batch server  
      ```sh
      poetry run uvicorn batch.main:app --reload
      ```

# lint, test
* client  
    ```sh
    cd client
    # linting
    npm run lint
    npm run format
    # testing
    npm run test
    ```
* server  
    ```sh
    cd server
    # linting
    poetry run ruff format .
    poetry run ruff check . --fix
    # testing
    poetry run pytest
    ```


# --------------------------------------------------
# for client build
# --------------------------------------------------
FROM node:20-alpine AS client-build
WORKDIR /app
COPY client/ /app/
RUN npm ci && \
    npm run build

# --------------------------------------------------
# for base
# --------------------------------------------------
FROM python:3-slim AS app-base

WORKDIR /app/server
COPY server/ /app/server/
COPY --from=client-build /app/build /app/client/build

RUN apt update && \
    apt install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone && \
    apt clean && \
    pip install poetry && \
    poetry install --without test,lint

# --------------------------------------------------
# for development
# --------------------------------------------------
FROM app-base AS app-dev
CMD ["poetry", "run", "uvicorn", "rest_api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# --------------------------------------------------
# for production
# --------------------------------------------------
FROM app-base AS app-prod
CMD ["poetry", "run", "uvicorn", "rest_api.main:app", "--host", "0.0.0.0", "--port", "80"]


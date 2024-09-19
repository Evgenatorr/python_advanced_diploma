docker exec -it fastapi_tweeter_clone alembic revision --autogenerate -m "create database"
docker exec -it fastapi_tweeter_clone alembic upgrade head
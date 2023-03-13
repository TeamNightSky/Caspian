(mkdir docker/volumes/db/data && echo "Created data folder.") || echo "Found data folder."

docker-compose up --build


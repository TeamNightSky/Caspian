mkdir docker/volumes/db/data &> /dev/null && echo "Created data folder." || echo "Found data folder."

docker-compose up --build


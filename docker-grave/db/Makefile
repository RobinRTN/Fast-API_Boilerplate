# Variables
DOCKER_IMAGE_NAME = postgres-img
DOCKER_CONTAINER_NAME = postgres-container
POSTGRES_USER = dev_user
POSTGRES_DB = dev_db
POSTGRES_PASSWORD = dev_password
POSTGRES_PORT = 5432
DB_FILE = /docker-entrypoint-initdb.d/init.sql

# Build the Docker image
build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d --name $(DOCKER_CONTAINER_NAME) \
		-e POSTGRES_USER=$(POSTGRES_USER) \
		-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		-e POSTGRES_DB=$(POSTGRES_DB) \
		-p $(POSTGRES_PORT):5432 \
		$(DOCKER_IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(DOCKER_CONTAINER_NAME)

up:
	docker start $(DOCKER_CONTAINER_NAME)

# Clean up the container and image
clean:
	docker rm -f $(DOCKER_CONTAINER_NAME) || true
	docker rmi -f $(DOCKER_IMAGE_NAME) || true

# Execute a command inside the running container
exec:
	docker exec -it $(DOCKER_CONTAINER_NAME) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) 

uri:
	@echo "postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@backend:$(POSTGRES_PORT)/$(POSTGRES_DB)"

save:
	docker exec -it db pg_dump -U dev_user -d dev_db > init.sql

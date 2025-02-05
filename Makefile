# Define variables for common configurations
REGISTRY=robinrtn
VERSION=latest

# Build and push all images
.PHONY: build-and-push
build-and-push:
	@echo "Building frontend..."
	make frontend
	@echo "Building backend..."
	make backend
	@echo "Building scrapers..."
	make scraper

# Backend image
.PHONY: backend
backend:
	docker build -t $(REGISTRY)/backend:$(VERSION) ./backend
	docker push $(REGISTRY)/backend:$(VERSION)

# Scraper image
.PHONY: scraper
scraper:
	docker build -t $(REGISTRY)/scraper:$(VERSION) ./scraper
	docker push $(REGISTRY)/scraper:$(VERSION)

# Frontend production image (Renamed from frontend_production to frontend)
.PHONY: frontend
frontend:
	docker build --build-arg VITE_APP_PRODUCTION=production -t $(REGISTRY)/frontend:$(VERSION) ./frontend
	docker push $(REGISTRY)/frontend:$(VERSION)

.PHONY: clean_containers
clean_containers:
	docker stop $$(docker ps -aq) || true
	docker rm $$(docker ps -aq) || true

# Remove all Docker images
.PHONY: clean_images
clean_images:
	docker rmi -f $$(docker images -aq) || true

# Remove all unused volumes
.PHONY: clean_volumes
clean_volumes:
	docker volume rm $$(docker volume ls -q) || true

# Remove all unused networks (except default)
.PHONY: clean_networks
clean_networks:
	docker network rm $$(docker network ls -q) || true

# Perform a complete system prune
.PHONY: full_clean
full_clean:
	docker system prune -a --volumes -f

# Run all cleanup steps
.PHONY: clean_all
clean_all: clean_containers clean_images clean_volumes clean_networks full_clean
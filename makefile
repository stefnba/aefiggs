#!make


# Start development containers
docker-up:
	docker compose --project-directory . -f docker/docker-compose.dev.yml up -d --build --force-recreate --remove-orphans
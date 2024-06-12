#!make

# Docker
# We must include the .env file for postgres since postgres init scripts needs it on build time
docker-up:
	docker compose -f docker/docker-compose.deploy.yml --project-directory . up -d --build --force-recreate --remove-orphans


# Start only the database service, usually only needed for development
docker-up-db:
	docker compose --project-directory services/db -f  services/db/docker-compose.yml up -d --build --force-recreate --remove-orphans db
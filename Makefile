help:
	@echo "Usage:"
	@echo "  make dev       - Run backend in development mode"
	@echo "  make prod      - Run backend in production mode"
	@echo "  make logs      - Show container logs"
	@echo "  make down      - Stop and remove containers"
	@echo "  make restart   - Restart the services"
	@echo "  make rebuild   - Rebuild and start containers"

dev:
	docker-compose -f docker-compose.yml up --build

prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build --force-recreate

logs:
	docker-compose logs -f

down:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

restart:
	make down && make prod

rebuild:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build --force-recreate
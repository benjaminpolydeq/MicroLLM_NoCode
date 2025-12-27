.PHONY: help setup start stop restart logs test

help:
	@echo "MicroLLM SaaS - Commandes:"
	@echo "  make setup    - Configuration initiale"
	@echo "  make start    - Démarrer les services"
	@echo "  make stop     - Arrêter les services"
	@echo "  make logs     - Voir les logs"

setup:
	@cp .env.example .env
	@echo "✅ .env créé - configure-le avant make start"

start:
	docker-compose up -d
	@echo "✅ Services démarrés!"
	@echo "Frontend: http://localhost:8501"
	@echo "API: http://localhost:8000"

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

test:
	docker-compose exec backend pytest tests/ -v

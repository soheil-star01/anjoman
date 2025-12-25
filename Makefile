.PHONY: help setup up down logs restart build clean dev prod status

help: ## Show this help message
	@echo "Anjoman - Make Commands"
	@echo "======================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Setup environment file
	@./setup-env.sh

up: ## Start all services (production)
	@echo "🚀 Starting Anjoman..."
	@docker-compose up -d
	@echo "✅ Anjoman is running!"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend:  http://localhost:8000"

dev: ## Start all services (development mode with hot reload)
	@echo "🔧 Starting Anjoman in development mode..."
	@docker-compose -f docker-compose.dev.yml up

down: ## Stop all services
	@echo "🛑 Stopping Anjoman..."
	@docker-compose down
	@echo "✅ Services stopped"

restart: ## Restart all services
	@echo "🔄 Restarting Anjoman..."
	@docker-compose restart
	@echo "✅ Services restarted"

logs: ## View logs from all services
	@docker-compose logs -f

logs-backend: ## View backend logs only
	@docker-compose logs -f backend

logs-frontend: ## View frontend logs only
	@docker-compose logs -f frontend

build: ## Build/rebuild all containers
	@echo "🔨 Building containers..."
	@docker-compose build
	@echo "✅ Build complete"

rebuild: ## Rebuild and start all services
	@echo "🔨 Rebuilding and starting..."
	@docker-compose up --build -d
	@echo "✅ Services rebuilt and started"

clean: ## Stop services and remove containers, volumes, and images
	@echo "🧹 Cleaning up..."
	@docker-compose down -v --rmi local
	@echo "✅ Cleanup complete"

status: ## Show status of all services
	@docker-compose ps

shell-backend: ## Open shell in backend container
	@docker-compose exec backend bash

shell-frontend: ## Open shell in frontend container
	@docker-compose exec frontend sh

install-backend: ## Install backend dependencies manually
	@cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

install-frontend: ## Install frontend dependencies manually
	@cd frontend && npm install

run-backend: ## Run backend manually (no Docker)
	@cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

run-frontend: ## Run frontend manually (no Docker)
	@cd frontend && npm run dev

backup: ## Backup session data
	@echo "💾 Backing up sessions..."
	@tar -czf sessions-backup-$$(date +%Y%m%d-%H%M%S).tar.gz data/sessions/
	@echo "✅ Backup created"

test: ## Run tests (placeholder)
	@echo "🧪 Running tests..."
	@echo "⚠️  Tests not yet implemented"

prod: up ## Alias for 'up' - start production services


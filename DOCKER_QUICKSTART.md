# Docker Quick Start - Anjoman

The **fastest** way to run Anjoman using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- At least one LLM API key (OpenAI, Anthropic, or Mistral)

## 3-Step Quick Start

### 1. Setup Environment

```bash
./setup-env.sh
```

Or manually create `.env`:
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### 2. Start Anjoman

```bash
docker-compose up -d
```

Or use make:
```bash
make up
```

### 3. Open Anjoman

Open your browser to: **http://localhost:3000**

**That's it! You're running Anjoman! 🎉**

## Common Commands

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after changes
docker-compose up --build
```

### Using Make (Easier)

```bash
# Start services
make up

# Development mode (hot reload)
make dev

# Stop services
make down

# View logs
make logs

# Restart
make restart

# See all commands
make help
```

## Development Mode

For development with hot reload:

```bash
# Using Docker Compose
docker-compose -f docker-compose.dev.yml up

# Using Make
make dev
```

Changes to your code will automatically reload!

## Verify Installation

Check that services are running:

```bash
# Using Docker Compose
docker-compose ps

# Using Make
make status

# Check health
curl http://localhost:8000
```

Expected output:
```json
{"service":"Anjoman API","status":"running","version":"0.1.0"}
```

## Troubleshooting

### "Port already in use"

Stop other services on ports 3000 or 8000:

```bash
# Find what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### "Cannot connect to backend"

Check backend is running:
```bash
docker-compose logs backend
curl http://localhost:8000
```

### "API key not found"

Verify your `.env` file:
```bash
cat .env
```

Make sure it contains:
```env
OPENAI_API_KEY=sk-...
```

Restart services:
```bash
docker-compose restart
```

### Start Fresh

```bash
# Stop and remove everything
docker-compose down -v

# Rebuild from scratch
docker-compose up --build -d
```

## Accessing Containers

```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# View environment variables
docker-compose exec backend env
```

## Data Persistence

Session data is stored in `./data/sessions/` and persists between restarts.

### Backup Sessions

```bash
# Using Make
make backup

# Manual
tar -czf sessions-backup.tar.gz data/sessions/
```

### Restore Sessions

```bash
tar -xzf sessions-backup.tar.gz
```

## Production Deployment

On your server:

```bash
# 1. Clone repository
git clone <your-repo>
cd anjoman

# 2. Setup environment
echo "OPENAI_API_KEY=sk-..." > .env

# 3. Start services
docker-compose up -d

# 4. (Optional) Setup reverse proxy for SSL
```

See [DOCKER.md](DOCKER.md) for advanced production setup.

## Resource Usage

Check resource usage:

```bash
docker stats
```

Typical usage:
- **Backend**: ~200-500 MB RAM, minimal CPU
- **Frontend**: ~100-200 MB RAM, minimal CPU

## Stopping and Cleanup

### Stop Services (Keep Data)

```bash
docker-compose stop
```

### Stop and Remove Containers

```bash
docker-compose down
```

### Remove Everything (Including Data)

```bash
# Warning: This deletes all session data!
docker-compose down -v
rm -rf data/sessions/*
```

## Next Steps

1. **Create your first session** at http://localhost:3000
2. **Read [DOCKER.md](DOCKER.md)** for advanced Docker usage
3. **See [README.md](README.md)** for project philosophy
4. **Check [ARCHITECTURE.md](ARCHITECTURE.md)** for technical details

## Why Docker?

✅ **One command to start everything**  
✅ **Consistent environment everywhere**  
✅ **No manual dependency installation**  
✅ **Easy deployment to production**  
✅ **Isolated and clean**  

## All Available Make Commands

```bash
make help          # Show all commands
make setup         # Setup .env file
make up            # Start production services
make dev           # Start development services
make down          # Stop services
make logs          # View all logs
make logs-backend  # View backend logs
make logs-frontend # View frontend logs
make restart       # Restart services
make build         # Build containers
make rebuild       # Rebuild and restart
make clean         # Remove everything
make status        # Show service status
make backup        # Backup session data
```

## Need Help?

- **Docker Issues**: See [DOCKER.md](DOCKER.md)
- **Setup Issues**: See [SETUP.md](SETUP.md)
- **General Questions**: See [README.md](README.md)
- **Report Bugs**: Open a GitHub issue

---

**Happy Deliberating! 🐳**


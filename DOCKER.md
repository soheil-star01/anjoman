# Docker Setup for Anjoman

Run Anjoman with Docker Compose for easy deployment and consistent environments.

## Quick Start with Docker

### Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

### 1. Setup Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
MISTRAL_API_KEY=your-key-here
```

### 2. Run with Docker Compose

**Production mode:**

```bash
docker-compose up -d
```

**Development mode (with hot reload):**

```bash
docker-compose -f docker-compose.dev.yml up
```

### 3. Access Anjoman

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Stop Services

```bash
docker-compose down
```

To also remove volumes (session data):

```bash
docker-compose down -v
```

## Docker Compose Configurations

### Production (`docker-compose.yml`)

- Optimized builds
- Production-ready images
- Minimal layers
- Persistent session storage
- Health checks
- Auto-restart on failure

**Usage:**
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development (`docker-compose.dev.yml`)

- Hot reload for both backend and frontend
- Source code mounted as volumes
- Faster iteration
- Better for local development

**Usage:**
```bash
# Start development services
docker-compose -f docker-compose.dev.yml up

# Rebuild after dependency changes
docker-compose -f docker-compose.dev.yml up --build
```

## Docker Commands Cheat Sheet

### Starting Services

```bash
# Start in background
docker-compose up -d

# Start with build
docker-compose up --build

# Start specific service
docker-compose up backend
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Managing Containers

```bash
# List running containers
docker-compose ps

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# Remove containers
docker-compose down
```

### Rebuilding

```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild and start
docker-compose up --build
```

### Accessing Containers

```bash
# Execute command in backend
docker-compose exec backend bash

# Execute command in frontend
docker-compose exec frontend sh

# View backend logs
docker-compose exec backend tail -f /app/logs/app.log
```

## Volume Management

### Session Data

Session data is persisted in `./data/sessions` which is mounted into the backend container.

**Backup sessions:**
```bash
tar -czf sessions-backup.tar.gz data/sessions/
```

**Restore sessions:**
```bash
tar -xzf sessions-backup.tar.gz
```

### Clear All Data

```bash
docker-compose down -v
rm -rf data/sessions/*
```

## Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:

**Option 1**: Stop the conflicting service

**Option 2**: Change ports in `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Use port 8001 instead
  frontend:
    ports:
      - "3001:3000"  # Use port 3001 instead
```

### Backend Can't Connect to LLM APIs

Check your API keys in `.env`:
```bash
docker-compose exec backend env | grep API_KEY
```

### Frontend Can't Connect to Backend

Check the `NEXT_PUBLIC_API_URL` environment variable:

```bash
docker-compose exec frontend env | grep NEXT_PUBLIC_API_URL
```

For local access from browser, make sure it's set to `http://localhost:8000`.

### Container Won't Start

View logs:
```bash
docker-compose logs backend
docker-compose logs frontend
```

Rebuild from scratch:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Permission Issues with Volumes

If you get permission errors with session files:

```bash
# Fix permissions
sudo chown -R $USER:$USER data/sessions/
chmod -R 755 data/sessions/
```

## Production Deployment

### Using Docker Compose on a Server

1. **Install Docker on your server**

2. **Clone the repository**
   ```bash
   git clone <your-repo>
   cd anjoman
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   nano .env  # Add your API keys
   ```

4. **Start services**
   ```bash
   docker-compose up -d
   ```

5. **Set up reverse proxy** (optional, recommended)
   
   Use Nginx or Traefik to add SSL and domain names.

### Environment-Specific Configs

Create additional compose files for different environments:

**docker-compose.prod.yml:**
```yaml
version: '3.8'
services:
  backend:
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=warning
  frontend:
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

**Usage:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build images
        run: docker-compose build
      
      - name: Push to registry
        run: |
          docker tag anjoman-backend:latest registry.example.com/anjoman-backend:latest
          docker push registry.example.com/anjoman-backend:latest
```

## Resource Limits

To limit resource usage, add to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Health Checks

Both services include health checks. View status:

```bash
docker-compose ps
```

Healthy services show `(healthy)` in the status.

## Logs and Monitoring

### View Real-Time Logs

```bash
# All services
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Since specific time
docker-compose logs --since 2024-12-25T10:00:00
```

### Log Rotation

For production, configure log rotation in `docker-compose.yml`:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Updating Anjoman

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Benefits of Docker Setup

✅ **Consistent Environment**: Same setup on all machines  
✅ **Easy Deployment**: Single command to start everything  
✅ **Isolation**: Dependencies contained in containers  
✅ **Portability**: Run anywhere Docker runs  
✅ **Scalability**: Easy to scale services  
✅ **Version Control**: Docker images are versioned  

## Comparison: Docker vs Manual Setup

| Aspect | Manual Setup | Docker Setup |
|--------|-------------|--------------|
| Setup Time | ~10 minutes | ~2 minutes |
| Dependencies | Manual install | Automatic |
| Consistency | Varies by system | Identical everywhere |
| Cleanup | Manual | `docker-compose down` |
| Production | More setup | Production-ready |
| Learning Curve | Lower | Slightly higher |

## Next Steps

- Read [README.md](README.md) for project overview
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check [SETUP.md](SETUP.md) for manual setup (if preferred)

---

**You're now running Anjoman in Docker! 🐳**


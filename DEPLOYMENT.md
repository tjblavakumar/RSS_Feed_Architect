# RSS Architect Deployment Guide 🚀

This guide covers different ways to deploy and run RSS Architect.

## 🐳 Docker Deployment (Recommended)

Docker provides the easiest and most consistent deployment experience.

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+ (or docker-compose 1.29+)

### Quick Start
```bash
# 1. Make scripts executable (Linux/Mac)
chmod +x *.sh

# 2. Start the application
./start.sh
```

The application will be available at `http://localhost:8501`

### Docker Scripts

| Script | Purpose |
|--------|---------|
| `./start.sh` | Build and start the application |
| `./stop.sh` | Stop the application |
| `./build.sh` | Rebuild the Docker image |

### Docker Commands Reference

```bash
# View logs
docker-compose logs -f

# Restart application
docker-compose restart

# Stop and remove containers
docker-compose down

# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d

# Check container status
docker-compose ps
```

### Data Persistence

The Docker setup includes volume mounts for data persistence:
- `./data:/app/data` - Data directory
- `./feed_storage.db:/app/feed_storage.db` - SQLite database

Your data will persist between container restarts.

## 🐍 Python Virtual Environment

For development or when Docker isn't available.

### Prerequisites
- Python 3.11+
- pip package manager

### Setup
```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python run.py
# OR
streamlit run app.py --server.headless true
```

## 🌐 Production Deployment

### Docker with Reverse Proxy

For production deployment behind a reverse proxy (nginx, Apache, etc.):

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  rss-architect:
    build: .
    container_name: rss-architect-prod
    ports:
      - "127.0.0.1:8501:8501"  # Bind to localhost only
    volumes:
      - ./data:/app/data
      - ./feed_storage.db:/app/feed_storage.db
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STREAMLIT_SERVER_HEADLESS` | `true` | Run without browser auto-open |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | `false` | Disable usage statistics |
| `STREAMLIT_SERVER_PORT` | `8501` | Port to run on |
| `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` | Address to bind to |

## 🔧 Troubleshooting

### Common Issues

**Port 8501 already in use**
```bash
# Find process using port
lsof -i :8501
# Kill process
kill -9 <PID>
```

**Docker build fails**
```bash
# Clean Docker cache
docker system prune -a
# Rebuild with no cache
./build.sh
```

**Permission denied on scripts**
```bash
# Make scripts executable
chmod +x *.sh
```

**Database locked error**
```bash
# Stop application
./stop.sh
# Remove database lock (if exists)
rm -f feed_storage.db-wal feed_storage.db-shm
# Restart
./start.sh
```

### Performance Tuning

For high-traffic deployments:

1. **Increase worker processes** (not applicable to Streamlit)
2. **Use external database** (PostgreSQL instead of SQLite)
3. **Add caching layer** (Redis for session data)
4. **Load balancing** (multiple container instances)

### Monitoring

Health check endpoint: `http://localhost:8501/_stcore/health`

```bash
# Check application health
curl -f http://localhost:8501/_stcore/health

# Monitor logs
docker-compose logs -f --tail=100
```

## 📊 Resource Requirements

### Minimum Requirements
- **CPU**: 1 core
- **RAM**: 512MB
- **Storage**: 100MB + database growth
- **Network**: Internet access for RSS discovery

### Recommended Requirements
- **CPU**: 2 cores
- **RAM**: 1GB
- **Storage**: 1GB + database growth
- **Network**: Stable internet connection

## 🔒 Security Considerations

1. **Network Security**: Bind to localhost in production
2. **Database Security**: Secure SQLite file permissions
3. **Container Security**: Run as non-root user (implemented)
4. **Reverse Proxy**: Use HTTPS in production
5. **Rate Limiting**: Implement at reverse proxy level

## 📝 Maintenance

### Regular Tasks
- Monitor disk space (database growth)
- Check application logs
- Update Docker images periodically
- Backup database file

### Backup Strategy
```bash
# Backup database
cp feed_storage.db feed_storage.db.backup.$(date +%Y%m%d)

# Backup with Docker
docker-compose exec rss-architect cp /app/feed_storage.db /app/data/backup.db
```

### Updates
```bash
# Pull latest code
git pull

# Rebuild and restart
./build.sh
./start.sh
```
# Docker Quick Start Guide 🐳

Get RSS Architect running with Docker in under 2 minutes!

## Prerequisites Check

```bash
# Check if Docker is installed
docker --version

# Check if Docker Compose is installed
docker-compose --version
# OR
docker compose version
```

If not installed, visit: https://docs.docker.com/get-docker/

## 🚀 Launch in 3 Steps

### Step 1: Make Scripts Executable (Linux/Mac only)
```bash
chmod +x start.sh stop.sh build.sh
```

### Step 2: Start the Application
```bash
./start.sh
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:8501**

That's it! 🎉

## 🛑 Stop the Application

```bash
./stop.sh
```

## 📋 Common Commands

### View Logs
```bash
docker-compose logs -f
```
Press `Ctrl+C` to exit log view

### Restart Application
```bash
docker-compose restart
```

### Check Status
```bash
docker-compose ps
```

### Rebuild After Code Changes
```bash
./build.sh
./start.sh
```

## 🔍 Troubleshooting

### Application Won't Start
```bash
# Check if port 8501 is in use
lsof -i :8501

# View error logs
docker-compose logs
```

### Permission Denied
```bash
# Make scripts executable
chmod +x *.sh
```

### Container Already Exists
```bash
# Remove old container
docker-compose down
# Start fresh
./start.sh
```

## 📁 Data Location

Your RSS feed database is stored in:
- `./feed_storage.db` - Main database file
- `./data/` - Additional data directory

These persist between container restarts.

## 🔄 Update Application

```bash
# Stop current version
./stop.sh

# Pull latest code (if using git)
git pull

# Rebuild and start
./build.sh
./start.sh
```

## 💡 Tips

- **First Run**: May take 1-2 minutes to build the Docker image
- **Subsequent Runs**: Start in seconds using cached image
- **Data Safety**: Your database persists even if you remove the container
- **Port Change**: Edit `docker-compose.yml` to change port from 8501

## 🆘 Need Help?

1. Check logs: `docker-compose logs -f`
2. Verify Docker is running: `docker ps`
3. Check port availability: `lsof -i :8501`
4. Read full deployment guide: `DEPLOYMENT.md`

## 🎯 What's Next?

Once running:
1. Enter a website URL (e.g., `https://example.com`)
2. Click "🔍 Scan for Feeds"
3. Save discovered RSS feeds
4. View and manage feeds in "📚 View Feeds"

Happy RSS discovering! 📡
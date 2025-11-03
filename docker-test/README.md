# Docker Test Example

This is a simple Docker test to verify your setup works.

## Quick Start

```bash
# Build the image
docker build -t docker-test .

# Run the container
docker run -d -p 8888:80 --name test-app docker-test

# Check if it's running
docker ps

# View logs
docker logs test-app

# Test it (from server)
curl http://localhost:8888

# Stop and remove
docker stop test-app
docker rm test-app
```

## Access the App

After running the container, you can access it:

1. **From the server terminal**: `curl http://localhost:8888`
2. **From your browser**: Set up nginx proxy or SSH tunnel (see /root/docker-guide.md)

## What This Demonstrates

✅ Docker builds images on the Scaleway server
✅ Containers run on the Scaleway server  
✅ You control everything from code-server
✅ Full Docker functionality available

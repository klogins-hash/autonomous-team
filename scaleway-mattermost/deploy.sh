#!/bin/bash

# Scaleway Mattermost Serverless Container Deployment Script

# Set variables
NAMESPACE="mattermost-ns"
CONTAINER_NAME="mattermost-app"
REGION="fr-par-1"

echo "Deploying Mattermost to Scaleway Serverless Containers..."

# Create namespace (if it doesn't exist)
echo "Creating namespace: $NAMESPACE"
scw container namespace create name=$NAMESPACE region=$REGION || echo "Namespace may already exist"

# Get namespace ID
NAMESPACE_ID=$(scw container namespace list name=$NAMESPACE region=$REGION --no-table | head -1 | awk '{print $1}')
echo "Namespace ID: $NAMESPACE_ID"

# Build and push Docker image to Scaleway Container Registry
echo "Building Docker image..."
docker build -t mattermost-serverless:latest .

# You need to create a Scaleway Container Registry first
# Uncomment and modify these lines once you have a registry
# REGISTRY_NAMESPACE="your-registry-namespace"
# docker tag mattermost-serverless:latest rg.$REGION.scw.cloud/$REGISTRY_NAMESPACE/mattermost:latest
# docker push rg.$REGION.scw.cloud/$REGISTRY_NAMESPACE/mattermost:latest

# Create container (using public image for demo)
echo "Creating container: $CONTAINER_NAME"
scw container container create \
  name=$CONTAINER_NAME \
  namespace-id=$NAMESPACE_ID \
  image=mattermost/mattermost-team-edition:10.11.5 \
  port=8080 \
  min-scale=1 \
  max-scale=3 \
  memory-limit=1024 \
  cpu-limit=500 \
  timeout=30s \
  privacy=public \
  region=$REGION \
  environment-variables="MM_SERVICESETTINGS_SITE_URL=https://mattermost-app.$NAMESPACE.containers.$REGION.scaleway.com,MM_SQLSETTINGS_DRIVERNAME=postgres,MM_ADMINSETTINGS_ENABLE_OPEN_SERVER=true,MM_SERVICESETTINGS_LISTENANDADDRESS=:8080" || echo "Container may already exist"

# Deploy container
echo "Deploying container..."
scw container container deploy $CONTAINER_NAME region=$REGION

echo "Deployment completed!"
echo "Your Mattermost instance will be available at: https://mattermost-app.$NAMESPACE.containers.$REGION.scaleway.com"

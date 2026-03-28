#!/bin/bash
# Load environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Use the image we built previously or build it again if needed
# For simplicity, we'll use the --source method but we need to handle the Dockerfile correctly
# Since gcloud run deploy --source with --dockerfile might be version-dependent, 
# I'll use the build-then-deploy strategy which is more reliable.

IMAGE_TAG="gcr.io/$GOOGLE_CLOUD_PROJECT/hellomcp-agent"

# Build the image
cp Dockerfile.agent Dockerfile
gcloud builds submit --tag "$IMAGE_TAG" .
rm Dockerfile

# Deploy to Cloud Run
gcloud run deploy hellomcp-agent \
    --image "$IMAGE_TAG" \
    --set-env-vars "MCP_SERVER_URL=https://mcp-server-396631018769.us-central1.run.app/mcp,GOOGLE_API_KEY=$GOOGLE_API_KEY,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,APP_NAME=$APP_NAME" \
    --region "$GOOGLE_CLOUD_LOCATION" \
    --allow-unauthenticated \
    --quiet

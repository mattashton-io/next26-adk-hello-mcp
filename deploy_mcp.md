# Deploying the MCP Integration to Cloud Run

This project implements a Model Context Protocol (MCP) server alongside an AI Agent that connects to it. To support this architecture, the deployments are separated into two containers: the MCP Server and the AI Agent Client.

Follow these step-by-step instructions to deploy both components to Google Cloud Run.

## Prerequisites
*   Ensure you have the Google Cloud CLI (`gcloud`) installed and configured.
*   Ensure your `gcloud` target project is set.
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

## Step 1: Deploy the MCP Server

The MCP Server must be deployed first so that the AI Agent can be configured with its URL.

```bash
gcloud run deploy mcp-server \
    --source . \
    --dockerfile Dockerfile.server \
    --region us-central1 \
    --allow-unauthenticated
```
*Note: If your MCP Server does not need to be public in a production environment, you should omit `--allow-unauthenticated` and configure IAM permissions for the AI Agent to securely invoke it using an OIDC token.*

**Save the Service URL**: Once the deployment completes, the CLI will output a Service URL (e.g., `https://mcp-server-xxxxx-uc.a.run.app`).

## Step 2: Deploy the AI Agent

Deploy the AI agent application, passing the MCP Server URL you retrieved in Step 1. Remember to append `/mcp` to the URL.

```bash
# Replace <YOUR_MCP_SERVER_URL> with the URL from Step 1 (e.g., https://mcp-server-xxxxx-uc.a.run.app)
gcloud run deploy hellomcp-agent \
    --source . \
    --dockerfile Dockerfile.agent \
    --set-env-vars MCP_SERVER_URL=<YOUR_MCP_SERVER_URL>/mcp \
    --region us-central1 \
    --allow-unauthenticated
```

## Step 3: Verification

Once both deployments are successful, navigate to the Service URL of your **AI Agent**. Interact with the agent (e.g., via chat) and ask for a "greeting for [Your Name]". The agent should invoke the remote MCP server to fulfill your request!

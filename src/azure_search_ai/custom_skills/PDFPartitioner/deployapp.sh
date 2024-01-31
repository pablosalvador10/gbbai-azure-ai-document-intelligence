#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' ../../../../.env | xargs)

# Check the command line argument
if [ "$1" == "build" ]; then
    # Build the Docker image
    docker build -f src/azure_search_ai/custom_skills/pdf_chunking/Dockerfile -t customskill .
elif [ "$1" == "run" ]; then
    # Run the Docker container, mapping port 8000 to 8000 and setting environment variables
    docker run -p 8000:8000 -e AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=$AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT -e AZURE_DOCUMENT_INTELLIGENCE_KEY=$AZURE_DOCUMENT_INTELLIGENCE_KEY -e AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING customskill
elif [ "$1" == "up" ]; then
    az containerapp up -n customskill --ingress external --target-port 8000 \
        --env-vars AZURE_AI_KEY=$AZURE_AI_KEY STORAGE_CONNNECTION_STRING="$STORAGE_CONNNECTION_STRING" OPENAI_API_KEY=$OPENAI_API_KEY \
        --source .
else
    echo "Usage: $0 {build|run|up}"
fi
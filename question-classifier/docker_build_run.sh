#!/usr/bin/env bash

docker rm -f llm_app
set -x

docker build . --platform linux/amd64 -f Dockerfile -t llm_app:latest
docker run -d --restart unless-stopped -e GROQ_API_KEY -p 8000:8000 llm_app
#!/bin/bash

# Start backend server
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 7860 &

# Serve frontend
cd /app/frontend
pnpm dlx serve -s dist -l 3000

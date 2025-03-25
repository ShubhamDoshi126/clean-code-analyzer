# Code Analyzer Tool

A lightweight tool that analyzes React (JavaScript) or FastAPI (Python) code files and scores them on clean code practices, while also offering recommendations for improvement.

## Features

- Analyzes JavaScript (.js), React (.jsx), and Python (.py) files
- Scores code quality on a scale of 0-100
- Provides detailed breakdown of scores across 6 categories:
  - Naming conventions (10 points)
  - Function length and modularity (20 points)
  - Comments and documentation (20 points)
  - Formatting/indentation (15 points)
  - Reusability and DRY principles (15 points)
  - Best practices in web development (20 points)
- Offers 3-5 actionable recommendations for improving code quality
- Includes GitHub Action for automated code quality checks on PRs

## Project Structure

```
code-analyzer/
├── backend/               # FastAPI backend
│   ├── venv/              # Python virtual environment
│   └── main.py            # Backend API implementation
├── frontend/              # React frontend
│   ├── public/            # Static assets
│   ├── src/               # Source code
│   │   ├── components/    # React components
│   │   │   ├── ui/        # UI components
│   │   │   ├── FileUpload.tsx
│   │   │   └── ResultsDisplay.tsx
│   │   ├── lib/           # Utility functions
│   │   ├── App.tsx        # Main application component
│   │   └── main.tsx       # Entry point
│   └── package.json       # Dependencies and scripts
└── .github/workflows/     # GitHub Actions
    └── code-quality-check.yml  # Code quality check workflow
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- pnpm (or npm)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd code-analyzer/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn python-multipart
   ```

4. Start the backend server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The backend API will be available at http://localhost:8000.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd code-analyzer/frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install  # or npm install
   ```

3. Start the development server:
   ```bash
   pnpm run dev  # or npm run dev
   ```

The frontend will be available at http://localhost:5173.

## Usage

1. Open the frontend application in your browser (http://localhost:5173)
2. Upload a JavaScript (.js), React (.jsx), or Python (.py) file
3. Click "Analyze Code" to submit the file for analysis
4. View the results, including:
   - Overall score out of 100
   - Breakdown of scores by category
   - Specific recommendations for improvement

## API Endpoints

### `POST /analyze-code`

Analyzes a code file and returns a quality score with recommendations.

**Request:**
- Content-Type: multipart/form-data
- Body: file (JavaScript, JSX, or Python file)

**Response:**
```json
{
  "overall_score": 82,
  "breakdown": {
    "naming": 8,
    "modularity": 17,
    "comments": 20,
    "formatting": 12,
    "reusability": 10,
    "best_practices": 15
  },
  "recommendations": [
    "Avoid deeply nested components in your React render logic.",
    "Function 'calculateTotal' in app.py is too long—consider refactoring.",
    "Use camelCase for variable 'Total_Amount'."
  ]
}
```

## Hosting on Hugging Face Spaces or Other Services

### Hosting on Hugging Face Spaces

1. Create a new Space on Hugging Face:
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Docker" as the Space SDK
   - Fill in the required details and create the Space

2. Create a Dockerfile in your project:
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   # Install Node.js and npm
   RUN apt-get update && apt-get install -y \
       curl \
       gnupg \
       && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
       && apt-get install -y nodejs \
       && npm install -g pnpm

   # Copy backend files
   COPY backend/main.py /app/backend/
   
   # Install backend dependencies
   RUN pip install fastapi uvicorn python-multipart

   # Copy frontend files
   COPY frontend /app/frontend/

   # Build frontend
   WORKDIR /app/frontend
   RUN pnpm install
   RUN pnpm run build

   # Create start script
   WORKDIR /app
   COPY start.sh /app/
   RUN chmod +x /app/start.sh

   EXPOSE 7860
   
   CMD ["/app/start.sh"]
   ```

3. Create a start.sh script:
   ```bash
   #!/bin/bash
   
   # Start backend server
   cd /app/backend
   uvicorn main:app --host 0.0.0.0 --port 7860 &
   
   # Serve frontend
   cd /app/frontend
   pnpm dlx serve -s dist -l 3000
   ```

4. Push your code to the Hugging Face Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   cp -r code-analyzer/* YOUR_SPACE_NAME/
   cd YOUR_SPACE_NAME
   git add .
   git commit -m "Initial commit"
   git push
   ```

### Hosting on Render

1. Create a new Web Service on Render:
   - Go to [render.com](https://render.com/) and sign up/login
   - Click "New" and select "Web Service"
   - Connect your GitHub repository

2. Configure the service:
   - Set the build command: `cd backend && pip install -r requirements.txt && cd ../frontend && npm install && npm run build`
   - Set the start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables if needed

3. Create a requirements.txt file in the backend directory:
   ```
   fastapi
   uvicorn
   python-multipart
   ```

4. Update the frontend API URL to use a relative path or environment variable for production.

### Hosting on Vercel

For a frontend-only deployment (requires a separate backend deployment):

1. Push your code to a GitHub repository

2. Connect your repository to Vercel:
   - Go to [vercel.com](https://vercel.com/) and sign up/login
   - Import your GitHub repository
   - Configure the project:
     - Root Directory: `frontend`
     - Build Command: `npm run build`
     - Output Directory: `dist`

3. Set environment variables for the backend API URL

4. Deploy the project

## GitHub Action

The project includes a GitHub Action that automatically analyzes code quality on pull requests and commits to the main branch.

To use it in your own repository:

1. Copy the `.github/workflows/code-quality-check.yml` file to your repository
2. The action will run automatically on pull requests and pushes to the main branch
3. Results will be posted as a comment on pull requests

## Development

### Backend

The backend is built with FastAPI and includes:

- File upload handling
- Code analysis logic for JavaScript/JSX and Python files
- Scoring algorithm based on clean code practices
- JSON response with scores and recommendations

### Frontend

The frontend is built with React and includes:

- File upload component with validation
- Results display with visual score breakdown
- Responsive design for various screen sizes

## License

MIT

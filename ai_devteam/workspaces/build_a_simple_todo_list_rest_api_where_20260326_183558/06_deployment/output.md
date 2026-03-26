---
## DEPLOYMENT PACKAGE

**Project:** Todo List REST API with JWT Authentication  
**Prepared by:** Deployment Engineer Agent  
**Target Environment:** Docker + AWS Elastic Beanstalk  

### Dockerfile
```dockerfile
# Use official Python image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ /app/backend

# Expose port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml (if applicable)
```yaml
version: '3.9'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/todo_db
      - JWT_SECRET_KEY=your_jwt_secret_key
      - JWT_EXPIRATION_MINUTES=60
    depends_on:
      - db
    command: uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: todo_db
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

### CI/CD Pipeline: .github/workflows/deploy.yml
```yaml
name: Deploy Todo List API

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest backend/tests --disable-warnings

      - name: Build Docker image
        run: docker build -t todo-list-api .

      - name: Push Docker image to AWS ECR
        id: ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Tag and push Docker image
        run: |
          IMAGE_TAG=todo-list-api:latest
          docker tag todo-list-api:latest ${{ steps.ecr.outputs.registry }}/$IMAGE_TAG
          docker push ${{ steps.ecr.outputs.registry }}/$IMAGE_TAG

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Deploy to AWS Elastic Beanstalk
        uses: einaregilsson/beanstalk-deploy@v20
        with:
          application_name: TodoListAPI
          environment_name: TodoListAPI-env
          version_label: ${{ github.sha }}
          region: us-east-1
          deployment_package: ./Dockerrun.aws.json
```

### Environment Variables
| Variable             | Description                                   | Example Value                  | Secret? |
|----------------------|-----------------------------------------------|--------------------------------|---------|
| DATABASE_URL         | Connection string for PostgreSQL database    | postgresql://user:password@db:5432/todo_db | Yes     |
| JWT_SECRET_KEY       | Secret key for signing JWT tokens            | your_jwt_secret_key            | Yes     |
| JWT_EXPIRATION_MINUTES | JWT token expiration time in minutes        | 60                             | No      |

### Deployment Instructions
**Prerequisites:**
- Docker installed locally.
- AWS Elastic Beanstalk CLI configured.
- AWS ECR repository created for Docker images.

**Step-by-step deployment:**
1. Clone the repository and navigate to the project directory.
2. Build the Docker image:
   ```bash
   docker build -t todo-list-api .
   ```
3. Push the Docker image to AWS ECR:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   docker tag todo-list-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/todo-list-api:latest
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/todo-list-api:latest
   ```
4. Deploy to AWS Elastic Beanstalk:
   ```bash
   eb init -p docker TodoListAPI --region us-east-1
   eb create TodoListAPI-env
   eb deploy
   ```

### Health Check
**Endpoint:** `/health`  
**Expected Response:**  
```json
{
  "status": "healthy"
}
```
- The `/health` endpoint should return a 200 status code and the above JSON response.

### Rollback Procedure
1. Identify the previous deployment version in AWS Elastic Beanstalk.
2. Use the following command to roll back:
   ```bash
   eb deploy --version <previous_version_label>
   ```
3. Verify the rollback by checking the `/health` endpoint.

---
**Status:** COMPLETE — Ready for QA / UAT Validator.
---
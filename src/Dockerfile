# Use an official Python image from Docker Hub
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

CMD ["uvicorn", "src.app_api_handler:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


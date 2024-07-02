# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY pyproject.toml poetry.lock /code/
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy project
COPY . /code/

# Change to the Django project directory
WORKDIR /code/personal_assistant

# Expose the port the app runs on
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

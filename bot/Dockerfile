# Use an official Python runtime as the base image
FROM python:3

# Set the working directory to /app
RUN mkdir /bot

# Copy the lockfile and pyproject.toml
COPY poetry.lock pyproject.toml /

# Install Poetry and dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Copy the application code
COPY ./ /bot

# Collect the static files
WORKDIR /bot

# Запускаем приложение
CMD ["python", "bot.py"]
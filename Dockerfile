# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# RUN python manage.py makemigrations --no input
# RUN python manage.py migrate --no input

# Copy project
COPY . /code/

# Expose the port
EXPOSE 8000

# Run migrations and start server
CMD ["gunicorn", "to_do.wsgi:application", "--bind", "0.0.0.0:8000"]

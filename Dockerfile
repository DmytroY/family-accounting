# official lightweight Python image
FROM python:3.11-slim

# do not precreate .pyc files. Do not buffer output - instant logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# working directory inside the container
WORKDIR /app

# Install system dependencies (needed for some Python packages and PostgreSQL support later)  !!! explain!!!
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# cash requirements only, RUN pip install only if requirements.txt was changed
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . /app/

# collectstatic require DJANGO_SECRET_KEY but do not check it, so dummy one used here.
# real key will be injected as docker env var at launch
RUN DJANGO_SECRET_KEY=dummy_key_for_build python3 family_acc/manage.py collectstatic --noinput

# Expose the port Gunicorn will run on
EXPOSE 8000


# Start the application using Gunicorn
# Using the path structure: --pythonpath family_acc family_acc.wsgi
CMD ["gunicorn", "--pythonpath", "family_acc", "family_acc.wsgi", "--bind", "0.0.0.0:8000"]

# start with development Django server
# CMD ["python3", "family_acc/manage.py", "runserver", "0.0.0.0:8000"]
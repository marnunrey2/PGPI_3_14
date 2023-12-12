# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Run management commands after copying the project

# Automate the flushing of the database by simulating 'yes' ('y') to the flush confirmation prompt
#RUN echo "yes" | python manage.py flush

#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN python manage.py loaddata servicios.json
#RUN python manage.py loaddata especialistas.json

# Pull base image
FROM python:3.8

RUN apt-get -y update
RUN apt-get install -y sqlite3 libsqlite3-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

RUN python django_for_startups/manage.py migrate --noinput

ARG admin_username=admin
ARG admin_email=admin@example.com
ARG admin_password=password

RUN python django_for_startups/manage.py createsuperuser --no-input --nfkc_username ${admin_username} --nfkc_primary_email ${admin_email}

RUN yes ${admin_password} | python django_for_startups/manage.py changepassword ${admin_username}

EXPOSE 8000
CMD ["python", "django_for_startups/manage.py", "runserver", "0.0.0.0:8000"]

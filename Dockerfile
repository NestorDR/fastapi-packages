# Pull base image.
FROM python:3.10

# Create a folder code in the container and set it as working directory.
WORKDIR /code

# Just copy the file with the requirements into the /code directory.
COPY ./requirements.txt /code/requirements.txt

# Install required libraries within container
#  --no-cache-dir prevents that PIP download packages locally, as re-installations are not necessary
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the ./app directory inside the /code directory.
COPY ./app /code/app

# Copy databases
COPY ./packages.db /code
COPY ./sqlite.db /code

# Set environment variables
ENV FASTAPI_PACKAGES_DB_ENGINE=SQLite
ENV FASTAPI_SIMPLE_SECURITY_SECRET=8df2b351-59a0-4b5c-a85b-fd59a5db28a8

# Set the command to run the uvicorn server.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


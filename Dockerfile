ARG PYTHON_VERSION=3.10.9
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


FROM base AS builder
WORKDIR /tmp 
RUN pip install poetry
RUN poetry self add poetry-plugin-export
COPY pyproject.toml  /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --no-cache

FROM base AS runner

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/


## install dependencies
WORKDIR /app
COPY --from=builder /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# RUN pip install imgkit
RUN apt-get update
RUN apt-get install wkhtmltopdf -y

# switch to the non-privileged user to run the application
#USER root

# Copy the source code into the container
COPY . .

# Expose the port that the app listens on.
EXPOSE 8000


# Run the application
ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


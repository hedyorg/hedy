# syntax=docker/dockerfile:1

# This is a multi-stage Dockerfile for building and running Hedy.
# Building is done in Docker as well to make the build easily portable to
# containerized platforms, as well as to keep the context small (because node_modules...)

#----------------------------------------------------------------------
# [platform] Base platform image
#----------------------------------------------------------------------
FROM python:3.13-slim AS platform
RUN --mount=target=/var/cache/apt,type=cache  --mount=target=/var/lib/apt,type=cache \
    apt update &&  \
    apt install build-essential nodejs npm curl -y

#----------------------------------------------------------------------
# [builder] Build stage
#----------------------------------------------------------------------
FROM platform AS builder
WORKDIR /app

# Pretend to be on Heroku to get the production build
ENV DYNO=1

# First copy only requirements so that we can cache the pip install layer, which is slow to run.
COPY requirements.txt requirements-prod.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

# Install dependencies
COPY package.json package-lock.json /app
RUN --mount=type=cache,target=/root/.npm npm ci

# Then copy everything
COPY . /app
RUN doit run deploy

#----------------------------------------------------------------------
# [hedy] Hedy application image
#----------------------------------------------------------------------
FROM platform AS hedy
WORKDIR /app

# Pretend to be on Heroku to get the production build
ENV DYNO=1

# First copy only requirements so that we can cache the pip install layer, which is slow to run.
COPY requirements-prod.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements-prod.txt

# Install dependencies
COPY package.json package-lock.json /app
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev

# Exclude node_modules, it's huge and contains dev dependencies we don't need.
COPY --from=builder --exclude=node_modules /app /app

EXPOSE 8000
ENTRYPOINT ["gunicorn", "app:create_app()"]

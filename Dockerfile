# syntax=docker/dockerfile:1

# This is a multi-stage Dockerfile for building and running Hedy.
# Building is done in Docker as well to make the build easily portable to
# containerized platforms, as well as to keep the context small (because node_modules...)

#----------------------------------------------------------------------
# [platform] Minimal runtime platform image
#----------------------------------------------------------------------
FROM python:3.13-slim AS platform
RUN --mount=target=/var/cache/apt,type=cache  --mount=target=/var/lib/apt,type=cache \
    apt update &&  \
    apt install nodejs npm curl -y

# This is necessary to see the variable in downstream stages.
ENV SHORT_PYTHON_VERSION=3.13

#----------------------------------------------------------------------
# [builder] Build stage
#----------------------------------------------------------------------
FROM platform AS builder
WORKDIR /app

# Pretend to be on Heroku to get the production build (note this env is NOT copied to
# the runtime stage, it's purely for the build).
ENV DYNO=1

# First copy only requirements so that we can cache the pip install layer, which is slow to run.
COPY requirements.txt requirements-prod.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

# Install dependencies
COPY package.json package-lock.json /app
RUN --mount=type=cache,target=/root/.npm npm ci

# Then copy everything and do the build step.
COPY . /app
RUN doit run deploy

#----------------------------------------------------------------------
# [dependencies] Image to install *production* dependencies.
#
# - Not a straight directory copy, because only want runtime dependencies,
#   not devDependencies
# - Not a reinstall, because we need 'build-essentials'  to install but not to run
#   and those dependencies are quite large.
#----------------------------------------------------------------------
FROM platform AS dependencies
RUN --mount=target=/var/cache/apt,type=cache  --mount=target=/var/lib/apt,type=cache \
    apt update &&  \
    apt install build-essential nodejs npm curl -y

WORKDIR /app

# First copy only requirements so that we can cache the pip install layer, which is slow to run.
COPY --from=builder /app/requirements-prod.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements-prod.txt

# Install dependencies
COPY --from=builder /app/package.json /app/package-lock.json /app
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev

#----------------------------------------------------------------------
# [hedy] Hedy application image
#----------------------------------------------------------------------
FROM platform AS hedy
WORKDIR /app

# Copy build artifacts from 'builder'
COPY --from=builder --exclude=node_modules /app /app

# Copy dependencies artifacts from 'dependencies'
COPY --from=dependencies /app/node_modules /app/node_modules
COPY --from=dependencies /usr/local/lib/python${SHORT_PYTHON_VERSION}/site-packages /usr/local/lib/python${SHORT_PYTHON_VERSION}/site-packages
# Copy the Python scripts that pip installed to /usr/local/bin, which is not in site-packages but is where the gunicorn executable is.
COPY --from=dependencies /usr/local/bin /usr/local/bin

EXPOSE 8000

ENTRYPOINT ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:8000"]

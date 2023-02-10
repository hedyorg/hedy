FROM python:3.9-slim as main

# use a non-root user (https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user)
ARG USERNAME=hedy
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install all binary dependencies (things that won't change due to our code changes)
# git is needed / useful in github codespaces
# make and gcc are needed for node-gyp package
RUN apt-get install -y gcc git make g++ curl && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt-get install -y nodejs

# Fix cypress dependencies
# https://docs.cypress.io/guides/continuous-integration/introduction#Dependencies
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y --no-install-recommends \
    libgtk2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 xauth xvfb

FROM main as node_builder
WORKDIR /app
COPY package* .
RUN npm ci

FROM main

# Setup python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy node modules to a tmp folder
COPY --from=node_builder /app/node_modules /var/tmp/node_modules

EXPOSE 8080
ENV SHELL /bin/bash
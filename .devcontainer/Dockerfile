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
RUN apt update && apt install -y gcc git curl && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt-get install -y nodejs


FROM main as node_builder
# Needed for node-gyp
RUN apt install -y make g++
WORKDIR /app
COPY package* .
RUN npm ci

FROM main

# Setup python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

# Copy node modules
COPY --from=node_builder /app/node_modules node_modules

COPY . .

# Fix translations
RUN pybabel compile -f -d translations

ENV BASE_URL=http://localhost:8080/

EXPOSE 8080
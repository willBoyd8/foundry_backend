FROM python:3.7.4 as python

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3 \
 && ln -s ~/.poetry/bin/poetry /usr/bin/poetry

# Get the source
COPY . /source
WORKDIR /source

# Build the source
RUN poetry build

# Build the actual runtime
FROM phusion/baseimage

# Copy the package, start script, and config to the new filesystem
COPY --from=python /source/deploy/start.sh /etc/service/foundry_backend/run
COPY --from=python /source/dist/*.tar.gz /foundry.tar.gz
COPY --from=python /source/deploy/settings.yaml /etc/foundry/settings.yaml
COPY --from=python /source/deploy/default_permissions.json /etc/foundry/permissions.json

# Set any Foundry environment variables
ENV FOUNDRY_SETTINGS "/etc/foundry/settings.yaml"
ENV FOUNDRY_PERMISSIONS_JSON "/etc/foundry/permissions.json"

# Install and configure foundry_backend
RUN add-apt-repository --yes ppa:deadsnakes/ppa \
 && apt-get update && apt-get install -y python3.7 python3-pip --no-install-recommends \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
 && python3.7 -m pip install setuptools wheel \
 && python3.7 -m pip install /foundry.tar.gz \
 && rm -rf /foundry.tar.gz \
 && chmod +x /etc/service/foundry_backend/run

RUN mkdir -p /opt/foundry/static && mkdir -p /opt/foundry/persistent
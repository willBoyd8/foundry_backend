FROM python:3.7.4 as python

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3 \
 && ln -s ~/.poetry/bin/poetry /usr/bin/poetry

# Get the source
COPY . /source
WORKDIR /source

# Build the source
RUN poetry build

# Move to the actual base
# It seems that the phusion/baseimage within dockerhub is
# old, and kaniko doesn't like that. We have to pull it from
# another repository to ensure it is accepted
FROM docker.abwlabs.com/phusion/baseimage

# Copy the package, start script, and config to the new filesystem
COPY --from=python /source/deploy/start.sh /etc/service/foundry_backend/run
COPY --from=python /source/dist/*.tar.gz /foundry.tar.gz
COPY --from=python /source/deploy/settings.yaml /etc/foundry/settings.yaml

# Set any Foundry environment variables
ENV FOUNDRY_SETTINGS "/etc/foundry/settings.yaml"

# Install and configure foundry_backend
RUN apt-get update && apt-get install -y python3-pip --no-install-recommends \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
 && pip3 install setuptools wheel \
 && pip3 install /foundry.tar.gz \
 && rm -rf /foundry.tar.gz \
 && chmod +x /etc/service/foundry_backend/run

RUN mkdir -p /opt/foundry/static
# foundry_backend
---
[![Build Status](https://jenkins.abwlabs.com/job/GitHub/job/foundry_backend/job/master/badge/icon)](https://jenkins.abwlabs.com/job/GitHub/job/foundry_backend/job/master/)

The backend component of Foundry MLS

`foundry_backend` is a Django server that maintains the database for Foundry MLS, as well as the API to interract with
the database. It is packaged for deployment as a Docker Image, or for a more fine tuned deployment, as a pip package.

## Configuration
Foundry needs configuration to be told how to run the system. By default, the configuration in `deploy/settings.yaml` is
used. Users can override this by placing their own settings files in `/opt/foundry/settings.yaml`. Environment
variables, in the format `FOUNDRY_<variable name>` can also be used to override variables defined in the `settings.yaml`
or `/opt/foundry/settings.yaml` files.

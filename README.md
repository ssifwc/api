# SSIFWC - API

This is a Python API deployed using the serverless framework as a AWS Lambda

## Endpoints

These are defined in the serverless.yml file and include the following:

- GET /watersheds
- GET /wells
- GET /parcels
- GET /springs
- GET /epicollect
- GET /aquifers
- GET /culverts
- GET /faults
- GET /greenwood
- POST /epicollect (returns a list of epicollect points by their uuids - used for the side panel)
- POST /image (uploads epicollect image to S3 using the epicollect ID)
- POST /metrics  (returns a list of metrics for a number of epicollect points using a given ID and radius)

## Setup

Install Serverless:

    npm install -g serverless
    
    
Install Serverless Python Requirements:

    sls plugin install -n serverless-python-requirements
    
Create a `serverless.env.yml` file which is used as part of the deployment process. Here is an example:

```buildoutcfg
dev:
  DATABASE_CONNECTION_URI: xxxxx
  EPICOLLECT_BASE_URL: xxxxx
  EPICOLLECT_PROJECT_NAME: xxxxx

```

## Deployment

Deployment requires only a simple serverless command, dependencies are installed automatically:

    sls deploy
 
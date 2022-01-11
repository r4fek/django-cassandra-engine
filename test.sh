#!/bin/bash

docker-compose up -d
docker-compose run web wait-for-it cassandra:9042 -- poetry run tox

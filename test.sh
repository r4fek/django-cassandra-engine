#!/bin/bash

docker compose up -d
docker compose run web wait-for-it cassandra:9042 -t 60 -- bash -c "cd testproject && poetry run python runtests.py"

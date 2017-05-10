#!/bin/bash
docker-compose stop loadbalancer
docker-compose rm -f loadbalancer
docker-compose up -d
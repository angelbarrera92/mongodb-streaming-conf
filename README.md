# mongodb-streaming-conf
An example app developed to learn and teach about streaming using mongodb collection


# Initializing the mongo server

```
docker run -p 27017:270017 -e "MONGODB_CAPPEDCOLLECTION=yes" mongo-capped:3.4
```

## Requirements
### Docker images
```
mongo:3.4
python:2.7-alpine
tutum/haproxy:latest
```
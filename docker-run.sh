#!/bin/bash
docker build -t base -f Dockerfile.base .
docker buil -t instagram .
docker run --rm -it -p 8013:80 instagram
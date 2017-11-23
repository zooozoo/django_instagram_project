#!/usr/bin/env bash
docker build -t base -f Dockerfile.base .
docker tag base shz0309/base
docker push shz0309/base
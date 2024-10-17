#!/bin/sh
cd app/
current_date=$(date +"%Y.%m.%d")
tag="taufikp/monitoring-psre:${current_date}"
echo $tag
docker build . -t $tag
docker push $tag
tag2="taufikp/monitoring-psre:latest"
docker build . -t $tag2
docker push $tag2

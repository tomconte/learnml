#!/bin/bash

set -e

if [ $# -ne 3 ]
then
  echo "args: registry image tag"
  exit 1
fi

registry=$1
image=$2
tag=$3

# Remove model if existing
rm -rf ./score/outputs ./score/score.py

# Download model
pushd ./score
python ../../azureml/download_model.py
popd

# Copy scoring script
cp ../topicmodel/score.py ./score

# Build image
docker build --tag ${registry}/${image}:${tag} .

# Push image
docker push ${registry}/${image}:${tag}

# Remove model & script
rm -rf ./score/outputs ./score/score.py

#!/bin/bash

registry=af10503475874c0380f75926f9d8df4c.azurecr.io
image=fn-topic-model
tag=24

# Remove model if existing
rm -rf ./score/outputs ./score/score.py

# Download model
pushd ./score
python ../../azureml/download_model.py
popd

# Copy scoring script
cp ../topicmodel/score.py ./score

# Build image
docker build --tag ${registry}/${image}:${tag} --build-arg function_code_path=${tmp_dir} .

# Remove model
rm -rf ./score/outputs ./score/score.py

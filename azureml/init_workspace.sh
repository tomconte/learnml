#!/bin/bash

# Create the workspace and initial components:
# - Compute cluster
# - Environment definition

# Args: prefix location

# Pre-requisites:
# - `az` CLI installed and logged in.
# - Python Azure ML SDK installed.

if [ $# -ne 2 ]
then
    echo "args: prefix location"
    exit 1
fi

prefix="$1"
location="$2"
sub_id=$(az account show --query id -o tsv)
rg_name="${prefix}-rg"
ws_name="${prefix}-ws"

# Add AML extension
echo '[ Adding ML extension to az CLI ]'
az extension add -n azure-cli-ml

# Create resource group
echo '[ Creating Resource Group ]'
az group create --name ${rg_name} --location ${location}

# Create AML workspace
echo '[ Creating Azure ML Workspace ]'
az ml workspace create -w ${ws_name} -g ${prefix}-rg

# Generate config.json
echo '[ Generating .azureml/config.json ]'
python -c "from azureml.core import Workspace; ws = Workspace('${sub_id}' , '${rg_name}', '${ws_name}'); ws.write_config()"

# Create Compute
echo '[ Creating Compute cluster ]'
python ./azureml/create_compute.py

# Create Environment
echo '[ Creating Environment definition ]'
python ./azureml/create_environment.py

import azureml.core
from azureml.contrib.functions import HTTP_TRIGGER, package
from azureml.core import Model, Workspace
from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig

env_name = 'gensim-environment'
model_name = 'gensim_lda'

print("Azure ML SDK Version: ", azureml.core.VERSION)

ws = Workspace.from_config()
print(ws.name, ws.location, ws.resource_group, sep='\t')

env = Environment.get(workspace=ws, name=env_name)

model = Model(workspace=ws, name=model_name)

inference_config = InferenceConfig(entry_script='./topicmodel/score.py', environment=env)

blob = package(ws, [model], inference_config, functions_enabled=True, trigger=HTTP_TRIGGER)

blob.wait_for_creation(show_output=True)

# Display the package location/ACR path
print(blob.location)

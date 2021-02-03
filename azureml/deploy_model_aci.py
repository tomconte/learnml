import azureml.core
from azureml.core import Workspace, Model
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core.webservice import AciWebservice

env_name = 'gensim-environment'
model_name = 'gensim_lda'

print("Azure ML SDK Version: ", azureml.core.VERSION)

ws = Workspace.from_config()
print(ws.name, ws.location, ws.resource_group, sep='\t')

env = Environment.get(workspace=ws, name=env_name)

model = Model(workspace=ws, name=model_name)

inference_config = InferenceConfig(
    entry_script='score.py',
    source_directory='./topicmodel',
    environment=env)

deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 1)

service = Model.deploy(ws, "topicservice", [model], inference_config, deployment_config, overwrite=True)

service.wait_for_deployment(show_output = True)

print(service.state)

import azureml.core
from azureml.core import Model, Workspace

model_name = 'gensim_lda'

print("Azure ML SDK Version: ", azureml.core.VERSION)

ws = Workspace.from_config()
print(ws.name, ws.location, ws.resource_group, sep='\t')

model = Model(workspace=ws, name=model_name)

model.download()

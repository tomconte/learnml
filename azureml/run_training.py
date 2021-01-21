import azureml.core
from azureml.core import Experiment, ScriptRunConfig, Workspace, Dataset
from azureml.core.environment import Environment

experiment_name = 'tm-gensim-20news'
compute_target_name = 'learnml-big'
env_name = 'gensim-environment'

print("Azure ML SDK Version: ", azureml.core.VERSION)

ws = Workspace.from_config()
print(ws.name, ws.location, ws.resource_group, sep='\t')

# Prepare experiment

exp = Experiment(workspace=ws, name=experiment_name)
compute_target = ws.compute_targets[compute_target_name]
env = Environment.get(workspace=ws, name=env_name)
ds = Dataset.get_by_name(workspace=ws, name='20news-train', version=2)

args = [
    '--input-data', ds.as_named_input('train_data'),
    '--num-topics', 10,
    '--chunksize', 2000,
    '--passes', 20,
    '--iterations', 400
]

src = ScriptRunConfig(source_directory="./topicmodel",
                      script='train.py', 
                      arguments=args,
                      compute_target=compute_target,
                      environment=env)

# Submit experiment

run = exp.submit(config=src)

run.wait_for_completion(show_output=True)

print(run.get_metrics())

print(run.get_file_names())

# Register model

model = run.register_model(model_name='gensim_lda', model_path='outputs')

print(model.name, model.id, model.version, sep='\t')

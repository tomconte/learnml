import azureml.core
from azureml.core import Dataset, Experiment, ScriptRunConfig, Workspace
from azureml.core.environment import Environment
from azureml.train.hyperdrive import (HyperDriveConfig, PrimaryMetricGoal,
                                      RandomParameterSampling, choice, normal,
                                      uniform)

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
    #'--num-topics', 10,
    '--chunksize', 2000,
    '--passes', 20,
    '--iterations', 400
]

src = ScriptRunConfig(source_directory="./topicmodel",
                      script='train.py',
                      arguments=args,
                      compute_target=compute_target,
                      environment=env)

param_sampling = RandomParameterSampling({
    "--num-topics": choice(5, 10, 15, 20)
})

# Submit experiment

hd = HyperDriveConfig(run_config=src,
                      hyperparameter_sampling=param_sampling,
                      primary_metric_name="c_v",
                      primary_metric_goal=PrimaryMetricGoal.MAXIMIZE,
                      max_total_runs=100,
                      max_concurrent_runs=4)

run = exp.submit(config=hd)

run.wait_for_completion(show_output=False)

print(run.get_metrics())

print(run.get_file_names())

# Register model

best_run = run.get_best_run_by_primary_metric()

model = best_run.register_model(model_name='gensim_lda', model_path='outputs')

print(model.name, model.id, model.version, sep='\t')

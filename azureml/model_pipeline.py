# pylint: disable=invalid-name

import azureml.core
from azureml.core import Dataset, Experiment, Workspace
from azureml.core.environment import Environment
from azureml.core.runconfig import RunConfiguration
from azureml.data import OutputFileDatasetConfig
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep

COMPUTE_TARGET_NAME = 'learnml-big'
ENV_NAME = 'gensim-environment'

print("Azure ML SDK Version: ", azureml.core.VERSION)

workspace = Workspace.from_config()
print(workspace.name, workspace.location, workspace.resource_group, sep='\t')

# Re-use pre-defined Compute Target and Environment

compute_target = workspace.compute_targets[COMPUTE_TARGET_NAME]
env = Environment.get(workspace=workspace, name=ENV_NAME)

# Step 1: data preparation

ds_20news_source = Dataset.File.from_files(
    path='http://qwone.com/~jason/20Newsgroups/20news-bydate.tar.gz')

train_ds = OutputFileDatasetConfig().read_delimited_files(separator='\t').register_on_complete(name='20news-train')

dataprep_step = PythonScriptStep(
    script_name="dataprep.py",
    source_directory="./topicmodel",
    compute_target=compute_target,
    arguments=[
        '--input', ds_20news_source.as_named_input('source').as_download(),
        '--output', train_ds
    ]
)

#ds = Dataset.get_by_name(workspace=workspace, name='20news-train', version=2)

# Step 2: Training

aml_run_config = RunConfiguration()
aml_run_config.target = compute_target
aml_run_config.environment = env

args = [
    '--input-data', train_ds.as_input(),
    '--num-topics', 10,
    '--chunksize', 2000,
    '--passes', 20,
    '--iterations', 400
]

train_step = PythonScriptStep(
    script_name='train.py',
    source_directory="./topicmodel",
    arguments=args,
    compute_target=compute_target,
    runconfig=aml_run_config,
    allow_reuse=True
)

# Build pipeline

pipeline_steps = [
    dataprep_step,
    train_step
]

pipeline = Pipeline(workspace=workspace, steps=[pipeline_steps])

# Run pipeline

run = Experiment(workspace=workspace, name='gensim_lda-pipeline').submit(pipeline)

run.wait_for_completion(show_output=True)

# Get training step

run_train_step = [s for s in run.get_steps() if s.name == 'train.py'][0]

print(run_train_step.get_metrics())
print(run_train_step.get_file_names())

# Register model

model = run_train_step.register_model(model_name='gensim_lda', model_path='outputs')

print(model.name, model.id, model.version, sep='\t')

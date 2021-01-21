from azureml.core import Workspace, Environment
from azureml.core.conda_dependencies import CondaDependencies

ws = Workspace.from_config()

# Start from minimal
my_env = Environment.get(workspace=ws, name="AzureML-Minimal")

# Rename the env
my_env.name = "gensim-environment"

# Add dependencies
conda_deps = CondaDependencies()
conda_deps.add_conda_package("gensim")
conda_deps.add_conda_package("nltk")

my_env.python.conda_dependencies = conda_deps

# Register the env
my_env.register(workspace=ws)

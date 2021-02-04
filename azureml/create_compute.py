from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute

ws = Workspace.from_config()

cpu_cluster_name = "learnml-big"

compute_config = AmlCompute.provisioning_configuration(
    vm_size='STANDARD_DS12_V2',
    max_nodes=2)

cpu_cluster = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

cpu_cluster.wait_for_completion(show_output=True)

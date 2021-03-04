# Topic Modeling with LDA on Azure Machine Learning

Experimenting with Topic Modeling using [Gensim's LDA implementation](https://radimrehurek.com/gensim//auto_examples/tutorials/run_lda.html) and the [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/) data set; running on [Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/).

![LDA-Viz](https://github.com/tomconte/learnml/raw/media/lda-viz.png)

## `azureml`

Contains the Python scripts used to train and deploy the model, using the Azure ML SDK.

- `create_environment.py`: create the Environment, mostly specifying the required Conda packages (`nltk` and `gensim`).
- `run_training_once.py`: train the model within an Experiment, with configurable parameters. Registers the resulting Model.
- `run_training_hyperdrive.py`: train the model using HyperDrive to compare different paramter values (e.g. number of topics).
- `deploy_model_aci.py`: deploy the model to ACI (suitable for testing).
- `deploy_model_function.py`: deploy the model to Functions (suitable for production).
- `download_model.py`: download the model locally; used to create the Docker image for custom Functions deployment.
- `model_pipeline.py`: create and run a pipeline consisting of data preparation and model training. Registers the resulting model.

## `topicmodel`

The data preparation, training and scoring scripts for the LDA model.

## `fn-topic-model`

A Function definition and build script that creates a custom Docker container image, ready to be deployed to a Function host. Alternative to deploying "natively" using Azure ML deployment capabilities.

## `terraform`

Terraform configuration for the Function host.

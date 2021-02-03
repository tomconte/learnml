terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "topicmodel" {
  name     = "${var.prefix}-rg"
  location = "westeurope"
}

resource "azurerm_storage_account" "topicmodel" {
  name                     = "${var.prefix}sa"
  resource_group_name      = azurerm_resource_group.topicmodel.name
  location                 = azurerm_resource_group.topicmodel.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "topicmodel" {
  name                = "${var.prefix}-service-plan"
  location            = azurerm_resource_group.topicmodel.location
  resource_group_name = azurerm_resource_group.topicmodel.name
  kind                = "elastic"
  reserved            = true

  sku {
    tier = "ElasticPremium"
    size = "EP1"
  }
}

resource "azurerm_function_app" "topicmodel" {
  name                       = "${var.prefix}-function"
  location                   = azurerm_resource_group.topicmodel.location
  resource_group_name        = azurerm_resource_group.topicmodel.name
  app_service_plan_id        = azurerm_app_service_plan.topicmodel.id
  storage_account_name       = azurerm_storage_account.topicmodel.name
  storage_account_access_key = azurerm_storage_account.topicmodel.primary_access_key
  os_type                    = "linux"
  version                    = "~3"

  site_config {
    linux_fx_version = "DOCKER|${var.docker_registry}/${var.docker_image}"
    cors {
      allowed_origins = ["*"]
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"          = "https://${var.docker_registry}"
    "DOCKER_REGISTRY_SERVER_USERNAME"     = var.docker_registry_username
    "DOCKER_REGISTRY_SERVER_PASSWORD"     = var.docker_registry_password
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = false
  }

  identity {
    type = "SystemAssigned"
  }
}

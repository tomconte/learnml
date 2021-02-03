variable "prefix" {
  type        = string
  description = "(optional) prefix for the resources"
  default     = "topicmodel2901"
}

variable "docker_registry" {
  description = "(mandatory)"
  type        = string
}

variable "docker_image" {
  description = "(mandatory)"
  type        = string
}

variable "docker_registry_username" {
  description = "(mandatory)"
  type        = string
}

variable "docker_registry_password" {
  description = "(mandatory)"
  type        = string
}

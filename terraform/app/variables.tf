variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "soat10tc-cluster-eks"
}

variable "vpc_cidr_block" {
  default = ["172.31.0.0/16"]
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "node_name" {
  default = "my-nodes-group"
}

variable "policy_arn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "instance_type" {
  default = "t3.small"
}

variable "db_password" {
  description = "Database user password"
  type        = string
}

variable "db_name" {
  default = "stock_microservice_db"
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "stock_microservice_api_key" {
  description = "Stock microservice API key"
  type        = string
}
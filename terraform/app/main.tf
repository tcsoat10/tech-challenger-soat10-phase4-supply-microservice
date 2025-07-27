provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc-stock-app"
    key    = "stock-microservice/terraform.tfstate"
    region = "us-east-1" # ajuste para sua região
  }
}

# data "terraform_remote_state" "aws" {
#   backend = "s3"
#   config = {
#     bucket = "soattc-aws-infra"
#     key    = "order-microservice/terraform.tfstate"
#     region = "us-east-1"
#   }
# }

# data "terraform_remote_state" "rds" {
#   backend = "s3"
#   config = {
#     bucket = "soattc-stock-db"
#     key    = "stock-microservice/terraform.tfstate"
#     region = "us-east-1"
#   }
# }

provider "kubernetes" {
  host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

resource "kubernetes_deployment" "stock_app" {
  metadata {
    name      = "stock-app"
    namespace = "default"
    labels = {
      app = "stock-app"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "stock-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "stock-app"
        }
      }
      spec {
        container {
          name  = "stock-app"
          image = "086134737169.dkr.ecr.us-east-1.amazonaws.com/soattc-stock-app:latest"
          env {
            name  = "MYSQL_HOST"
            value = replace(data.terraform_remote_state.rds.outputs.db_endpoint, ":3306", "")
          }
          env {
            name  = "MYSQL_USER"
            value = var.db_username
          }
          env {
            name  = "MYSQL_PASSWORD"
            value = var.db_password
          }
          env {
            name  = "MYSQL_PORT"
            value = "3306"
          }          
          env {
            name = "STOCK_MICROSERVICE_X_API_KEY"
            value = var.stock_microservice_api_key
          }
          env {
            name = "MYSQL_DATABASE"
            value = data.terraform_remote_state.rds.outputs.db_name
          }
          port {
            container_port = 8080
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "stock_app_lb" {
  depends_on = [kubernetes_deployment.stock_app]
  metadata {
    name      = "stock-app-lb"
    namespace = "default"
  }
  spec {
    selector = {
      app = "stock-app"
    }
    type = "LoadBalancer"
    port {
      port        = 80
      target_port = 8003
    }
  }
}
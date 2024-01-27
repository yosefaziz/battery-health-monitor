terraform {
  required_version = "~> 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "tf-battery-health-monitor"
    key    = "infra.tfstate"
    region = var.aws_region
  }
}

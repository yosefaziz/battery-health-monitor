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

module "aws_iam" {
  source = "./../../modules/aws/iam"
}

module "aws_lambda" {
  source    = "./../../modules/aws/lambda"
  role_arn  = module.aws_iam.lambda_role_arn
  policy_id = module.aws_iam.lambda_iam_policy_id
}

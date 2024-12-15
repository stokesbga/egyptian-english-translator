# IAM roles and policies
data "aws_iam_policy_document" "sagemaker_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sagemaker_access_iam_role" {
    name = "sagemaker_access_iam_role"
    path = "/system/"
  assume_role_policy = data.aws_iam_policy_document.sagemaker_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "sagemaker_access_policy_attachment" {
    role = aws_iam_role.sagemaker_access_iam_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

variable container_image {}

# Sagemaker Resources
resource "aws_sagemaker_model" "sagemaker-eg-en-translator-model" {
  name               = "sagemaker-eg-en-translator-model"
  execution_role_arn = aws_iam_role.sagemaker_access_iam_role.arn

  primary_container {
    image = var.container_image 
  }
}

resource "aws_sagemaker_endpoint_configuration" "eg-en-translator-endpoint-configuration" {
  name = "eg-en-translator-endpoint-configuration"

  production_variants {
    variant_name           = "en-eg-translator-variant"
    model_name             = aws_sagemaker_model.sagemaker-eg-en-translator-model.name
    initial_instance_count = 1
    instance_type          = "ml.t2.medium"
  }

  tags = {
    Name = "eg-en-translator-endpoint-configuration"
  }
}

resource "aws_sagemaker_endpoint" "eg-en-translator-endpoint" {
  name                 = "eg-en-translator-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.eg-en-translator-endpoint-configuration.name

  tags = {
    Name = "eg-en-translator-endpoint"
  }
}


# Outputs
output "sagemaker_endpoint_name" {
    value = aws_sagemaker_endpoint.eg-en-translator-endpoint.name
    description = "SageMaker Endpoint Name"
}

output "sagemaker_endpoint_arn" {
    value = aws_sagemaker_endpoint.eg-en-translator-endpoint.arn
    description = "SageMaker Endpoint ARN"
}

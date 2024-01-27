data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_dir  = "${path.module}/python/"
  output_path = "${path.module}/python/battery_health_monitor.zip"
}

# Lambda function
resource "aws_lambda_function" "battery_health_monitor" {
  filename         = "${path.module}/python/battery_health_monitor.zip"
  function_name    = "battery_health_monitor"
  role             = var.role_arn
  handler          = "battery_health_monitor.main"
  runtime          = "python3.11"
  timeout          = 10
  memory_size      = 128
  source_code_hash = data.archive_file.zip_the_python_code.output_base64sha256
  depends_on       = [var.policy_id]
}

resource "aws_cloudwatch_log_group" "battery_health_monitor" {
  name              = "/aws/lambda/${aws_lambda_function.battery_health_monitor.function_name}"
  retention_in_days = 1
}

output "lambda_role_name" {
  value = aws_iam_role.lambda_role.name
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}

output "lambda_iam_policy_id" {
  value = aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role.id
}

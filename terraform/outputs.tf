output "instance_id" {
  description = "ID of the AI inference EC2 instance"
  value       = aws_instance.ai_inference.id
}

output "public_ip" {
  description = "Public IP address of the AI inference EC2 instance"
  value       = aws_instance.ai_inference.public_ip
}

output "security_group_id" {
  description = "Security group attached to the AI inference instance"
  value       = aws_security_group.ai_inference.id
}
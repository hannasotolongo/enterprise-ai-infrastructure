variable "aws_region" {
  description = "AWS region used to deploy the AI infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type used for the inference server"
  type        = string
  default     = "t3.micro"
}
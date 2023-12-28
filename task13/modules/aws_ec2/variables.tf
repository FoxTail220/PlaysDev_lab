variable "instance_type" {
  description = "value from main variable.tf"
}

variable "vpc_public_sg_id" {
  description = "value from module aws_sg"
}

variable "vpc_private_sg_id" {
  description = "value from module aws_sg"
}

variable "public_subnet_ids" {
  description = "public subnet ids from aws_net module"
}

variable "private_subnet_ids" {
  description = "private subnet ids from aws_net module"
}

variable "env" {
  description = "env variable"
}

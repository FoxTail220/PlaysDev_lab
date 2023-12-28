variable "vpc_cidr" {
  description = "vpc cidr for main VPC"
}

variable "env" {
  description = "env variable"
}

variable "public_subnet_cidrs" {
  description = "cidrs for public subnet"
}

variable "private_subnet_cidrs" {
  description = "cidrs for private subnet"
}

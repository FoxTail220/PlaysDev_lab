variable "vpc_cidr" {
  default = "10.10.0.0/16"
}

variable "public_sub_cidrs" {
  type = list(string)
  default = [
    "10.10.1.0/24"
  ]
}

variable "private_sub_cidrs" {
  type = list(string)
  default = [
    "10.10.11.0/24"
  ]
}

variable "open_ports" {
  default = [
    "80",
    "443",
    "22"
  ]
}

variable "ec2_instance_type" {
  default = "t2.micro"
}

variable "enviroment" {
  default = "z-pam"
}


variable "user" {}
variable "password" {}

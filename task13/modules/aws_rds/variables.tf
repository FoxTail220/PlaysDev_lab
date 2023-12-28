variable "user" {}

variable "pass" {}

variable "class" {
  default = "db.t3.micro"
}

variable "eng" {
  default = "postgres"
}

variable "name" {
  default = "task13"
}

variable "az" {
  default = "eu-central-1a"
}


variable "db_name" {
  default = "task13_db"
}

variable "public_subnet_ids" {}

variable "private_subnet_ids" {}
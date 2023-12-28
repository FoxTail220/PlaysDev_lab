resource "aws_security_group" "task13_sg_private" {
  name        = "${var.env}_private_security_group"
  description = "${var.env}_security_group"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ports_open
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = [var.vpc_cidr]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" #any protocol
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name  = "private_${var.env}_SG"
    Owner = "Daniil L"
  }
}


resource "aws_security_group" "task13_sg_public" {
  name        = "${var.env}_public_security_group"
  description = "${var.env}_security_group"
  vpc_id      = var.vpc_id

  ingress {

    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" #any protocol
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name  = "public_${var.env}_SG"
    Owner = "Daniil L"
  }
}


 /*resource "aws_security_group" "rds_private" {
  name        = "${var.env}_task13_rds_sg_private"
  description = "${var.env}_security_group"
  vpc_id      = var.vpc_id

  ingress {

    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" #any protocol
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name  = "public_${var.env}_SG"
    Owner = "Daniil L"
  }
}

*/
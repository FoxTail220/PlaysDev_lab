provider "aws" {
  region = "eu-west-1"
}


resource "aws_instance" "Bastion" {
  ami           = "ami-0905a3c97561e0b69"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.bastion-host-sg.id]
  /* user_data = <<EOF
    скрипт сюда
    EOF
*/

  tags = {
    Name = "Bastion host"
  }
}

resource "aws_instance" "Private" {
  ami           = "ami-08031206a0ff5a6ac"
  instance_type = "t2.micro"

  tags = {
    Name = "Private host"
  }
}


resource "aws_security_group" "bastion-host-sg" {
  name = "Bastion host sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

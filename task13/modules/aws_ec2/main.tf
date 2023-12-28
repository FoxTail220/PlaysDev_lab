data "aws_ami" "latest_ubuntu" {
  owners = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20231207"]
  }
}


resource "aws_instance" "main_public" {
  count                  = length(var.public_subnet_ids)
  ami                    = data.aws_ami.latest_ubuntu.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [var.vpc_public_sg_id]
  subnet_id              = var.public_subnet_ids[count.index]
  key_name               = "task13"
  tags = {
    Name = "${var.env}_public_${count.index + 1}"
  }
}

resource "aws_instance" "main_private" {
  count                  = length(var.private_subnet_ids)
  ami                    = data.aws_ami.latest_ubuntu.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [var.vpc_private_sg_id]
  subnet_id              = var.private_subnet_ids[count.index]
  key_name               = "task13"

  tags = {
    Name = "${var.env}_private_${count.index + 1}"
  }
}

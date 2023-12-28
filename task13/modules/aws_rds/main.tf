resource "aws_db_subnet_group" "rds_subnet" {
  name       = "database subnets"
  subnet_ids = [var.private_subnet_ids, var.public_subnet_ids]
}

resource "aws_db_instance" "remote_db" {
  allocated_storage      = 20
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet.id
  db_name                = var.db_name
  engine                 = var.eng
  engine_version         = "15.4"
  instance_class         = var.class
  username               = var.user
  password               = var.pass
  availability_zone      = var.az
  skip_final_snapshot    = true
  publicly_accessible    = true
  
 
  tags = {
    Name = var.name
  }
}


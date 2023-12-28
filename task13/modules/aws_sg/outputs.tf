output "vpc_private_sg_id" {
  value = aws_security_group.task13_sg_private.id
}

output "vpc_public_sg_id" {
  value = aws_security_group.task13_sg_public.id
}

#output "rds-privatochka" {
 # value = aws_security_group.rds_private.id

#}

output "bastion_ips" {
  value = aws_instance.main_public[*].public_ip
}

output "private_ips" {
  value = aws_instance.main_private[*].private_ip
}

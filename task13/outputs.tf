output "dev_public_subnet_ids" {
  value = module.vpc-dev.public_subnet_ids
}

output "dev_private_subnet_ids" {
  value = module.vpc-dev.private_subnet_ids
}

output "bastion_ips" {
  value = module.ec2.bastion_ips
}

output "private_ips" {
  value = module.ec2.private_ips
}

output "rds_db_id" {
    value = module.rds.db_id
}
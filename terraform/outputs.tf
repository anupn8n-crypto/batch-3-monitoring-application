output "instance_id" {
  description = "EC2 instance ID for Anup_demo"
  value       = aws_instance.Anup_demo.id
}

output "public_ip" {
  description = "Ephemeral public IP of Anup_demo"
  value       = aws_instance.Anup_demo.public_ip
}

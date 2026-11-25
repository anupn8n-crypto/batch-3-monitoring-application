# Default VPC and its default security group
data "aws_vpc" "default" {
  default = true
}

data "aws_security_group" "default" {
  name   = "default"
  vpc_id = data.aws_vpc.default.id
}

# Default subnet in the requested AZ (needed to place the instance in us-east-1f)
data "aws_subnet" "default_1f" {
  vpc_id            = data.aws_vpc.default.id
  availability_zone = "us-east-1f"
  default_for_az    = true
}

resource "aws_instance" "Anup_demo" {
  ami                         = "ami-0fbc7ac82ff7690bc"
  instance_type               = "t3.micro"
  subnet_id                   = data.aws_subnet.default_1f.id
  vpc_security_group_ids      = [data.aws_security_group.default.id]
  associate_public_ip_address = true # ephemeral public IP

  availability_zone = "us-east-1f"

  tags = {
    Name = "Anup_demo"
  }
}

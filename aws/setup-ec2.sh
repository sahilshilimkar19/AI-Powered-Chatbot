#!/bin/bash
# AWS EC2 User Data / Setup Script
# Run this after SSH into your EC2 instance

set -e

echo "=== Updating system ==="
sudo yum update -y

echo "=== Installing Docker ==="
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

echo "=== Installing Docker Compose ==="
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "=== Installing Node.js 20 ==="
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs

echo "=== Installing Git ==="
sudo yum install -y git

echo "=== Installing Nginx ==="
sudo yum install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx

echo "=== Setup complete! ==="
echo "Log out and back in for Docker group to take effect."
echo "Then clone your repo and follow the deployment steps in DEPLOY_AWS.md"

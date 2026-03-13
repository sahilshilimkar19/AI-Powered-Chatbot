# AWS Free Tier Deployment Guide

Deploy the full AI Chatbot on AWS Free Tier using **EC2** (backend + frontend).

---

## Prerequisites

- AWS account (free tier eligible)
- Your OpenAI API key
- Project pushed to a Git repository (GitHub/GitLab)

---

## Step 1: Launch EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Configure:
   - **Name**: `ai-chatbot`
   - **AMI**: Amazon Linux 2023 (Free tier eligible)
   - **Instance type**: `t2.micro` (Free tier - 750 hrs/month)
   - **Key pair**: Create or select existing (download `.pem` file)
   - **Security Group**: Allow these inbound rules:
     | Type  | Port | Source    |
     |-------|------|-----------|
     | SSH   | 22   | Your IP   |
     | HTTP  | 80   | 0.0.0.0/0 |
     | HTTPS | 443  | 0.0.0.0/0 |
   - **Storage**: 8 GB gp3 (free tier)
3. Click **Launch Instance**

---

## Step 2: Connect to EC2

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

---

## Step 3: Run Setup Script

```bash
# Clone your repo
git clone https://github.com/your-username/ai-chatbot.git
cd ai-chatbot

# Run the setup script
chmod +x aws/setup-ec2.sh
./aws/setup-ec2.sh

# Log out and back in for Docker group
exit
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

---

## Step 4: Deploy Backend

```bash
cd ~/ai-chatbot/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
nano .env  # Set LLM_PROVIDER=groq and add your GROQ_API_KEY

# Test the backend
uvicorn main:app --host 0.0.0.0 --port 8000

# For production, use systemd service (see below)
```

### Create systemd service for auto-restart:

```bash
sudo tee /etc/systemd/system/chatbot-api.service > /dev/null <<EOF
[Unit]
Description=AI Chatbot API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/ai-chatbot/backend
Environment=PATH=/home/ec2-user/ai-chatbot/backend/venv/bin
ExecStart=/home/ec2-user/ai-chatbot/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable chatbot-api
sudo systemctl start chatbot-api

# Check status
sudo systemctl status chatbot-api
```

---

## Step 5: Build & Deploy Frontend

```bash
cd ~/ai-chatbot/frontend

# Install dependencies and build
npm install
VITE_API_URL=/api npm run build

# The built files are in dist/
```

---

## Step 6: Configure Nginx

```bash
# Copy nginx config
sudo cp ~/ai-chatbot/aws/nginx.conf /etc/nginx/conf.d/chatbot.conf

# Edit the server_name to your EC2 public IP or domain
sudo nano /etc/nginx/conf.d/chatbot.conf

# Remove default config if it exists
sudo rm -f /etc/nginx/conf.d/default.conf

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 7: Access Your Chatbot

Open your browser and go to:
```
http://<EC2-PUBLIC-IP>
```

---

## Optional: Add HTTPS with Let's Encrypt

```bash
# Install certbot
sudo yum install -y certbot python3-certbot-nginx

# Get certificate (requires a domain name pointing to your EC2 IP)
sudo certbot --nginx -d your-domain.com

# Auto-renew
sudo crontab -e
# Add: 0 2 * * * certbot renew --quiet
```

---

## Optional: Docker Deployment

Instead of manual setup, use Docker:

```bash
cd ~/ai-chatbot

# Build and run with Docker
docker build -t chatbot-api .
docker run -d \
  --name chatbot-api \
  -p 8000:8000 \
  -e LLM_PROVIDER=groq \
  -e GROQ_API_KEY=your-key-here \
  -e CORS_ORIGINS=http://your-ec2-ip \
  --restart always \
  chatbot-api
```

---

## Cost Breakdown (Free Tier)

| Service      | Free Tier Allowance         | Cost    |
|-------------|----------------------------|---------|
| EC2 t2.micro | 750 hours/month (12 months) | **$0**  |
| EBS (8 GB)   | 30 GB/month                 | **$0**  |
| Data Transfer | 100 GB/month out            | **$0**  |
| **Total**    |                             | **$0/month** |

> **Note**: Groq and Gemini APIs are free with rate limits. If using OpenAI, `gpt-3.5-turbo` costs ~$0.002/1K tokens.

---

## Troubleshooting

- **Backend not starting**: Check `sudo journalctl -u chatbot-api -f`
- **Nginx errors**: Check `sudo tail -f /var/log/nginx/error.log`
- **Can't connect**: Verify security group rules allow port 80
- **API errors**: Ensure `.env` has valid API key for your chosen provider (`GROQ_API_KEY`, `GEMINI_API_KEY`, or `OPENAI_API_KEY`)

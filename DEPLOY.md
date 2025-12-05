# Deployment Guide

## Local Development Deployment

### Prerequisites
- Python 3.8+
- pip package manager
- Modern web browser

### Steps

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python api.py
```

3. **Access the application:**
```
http://localhost:5000
```

## Production Deployment Options

### Option 1: Heroku Deployment

1. **Install Heroku CLI:**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Procfile:**
```bash
echo "web: gunicorn api:app" > Procfile
```

3. **Add gunicorn to requirements:**
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

4. **Deploy:**
```bash
heroku login
heroku create wind-loading-calculator
git init
git add .
git commit -m "Initial deployment"
git push heroku main
```

### Option 2: AWS EC2 Deployment

1. **Launch EC2 instance:**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier eligible)
   - Security group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

4. **Clone/upload project:**
```bash
cd /home/ubuntu
# Upload project files
```

5. **Setup virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

6. **Create systemd service:**
```bash
sudo nano /etc/systemd/system/windcalc.service
```

Add:
```ini
[Unit]
Description=Wind Loading Calculator
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/wind-loading-calculator
Environment="PATH=/home/ubuntu/wind-loading-calculator/venv/bin"
ExecStart=/home/ubuntu/wind-loading-calculator/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 api:app

[Install]
WantedBy=multi-user.target
```

7. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/windcalc
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

8. **Enable and start services:**
```bash
sudo ln -s /etc/nginx/sites-available/windcalc /etc/nginx/sites-enabled/
sudo systemctl start windcalc
sudo systemctl enable windcalc
sudo systemctl restart nginx
```

### Option 3: Docker Deployment

1. **Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "api:app"]
```

2. **Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: always
```

3. **Build and run:**
```bash
docker-compose up -d
```

### Option 4: Azure App Service

1. **Install Azure CLI:**
```bash
# Download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

2. **Login and create app:**
```bash
az login
az webapp up --name wind-loading-calculator --runtime "PYTHON:3.11"
```

3. **Configure startup command:**
```bash
az webapp config set --name wind-loading-calculator --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 api:app"
```

## Environment Configuration

### Production Settings

Create `.env` file:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Security Considerations

1. **HTTPS:** Always use HTTPS in production
2. **CORS:** Configure CORS for specific domains only
3. **Rate Limiting:** Add rate limiting to prevent abuse
4. **Input Validation:** Already implemented in API
5. **Logging:** Enable production logging

### Performance Optimization

1. **Use Gunicorn with multiple workers:**
```bash
gunicorn --workers 4 --threads 2 --bind 0.0.0.0:5000 api:app
```

2. **Enable caching for static files**

3. **Use CDN for static assets**

4. **Database:** Consider adding Redis for session storage

## Monitoring

### Health Check Endpoint

```bash
curl http://your-domain.com/api/health
```

Expected response:
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "standard": "BS EN 1991-1-4:2005+A1:2010"
}
```

### Logging

Add logging configuration to `api.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wind_calculator.log'),
        logging.StreamHandler()
    ]
)
```

## Backup and Maintenance

### Regular Tasks

1. **Update dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

2. **Check logs:**
```bash
tail -f wind_calculator.log
```

3. **Monitor disk space:**
```bash
df -h
```

4. **Restart service:**
```bash
sudo systemctl restart windcalc
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

2. **Permission denied:**
```bash
sudo chown -R ubuntu:ubuntu /home/ubuntu/wind-loading-calculator
```

3. **Module not found:**
```bash
pip install -r requirements.txt
```

4. **Nginx not serving:**
```bash
sudo nginx -t  # Test configuration
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

## SSL/TLS Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo systemctl reload nginx
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ELB, Nginx)
- Multiple application instances
- Shared session storage (Redis)

### Vertical Scaling
- Increase instance size
- More workers/threads
- Optimize calculation algorithms

## Cost Estimates

### AWS EC2 (t2.micro)
- **Cost:** ~$8-10/month
- **Suitable for:** Low to medium traffic

### Heroku (Hobby tier)
- **Cost:** $7/month
- **Suitable for:** Low traffic, easy deployment

### Azure App Service (B1)
- **Cost:** ~$13/month
- **Suitable for:** Medium traffic

## Support

For deployment assistance:
- **Email:** sales@nbnesigns.co.uk
- **Phone:** 01665 606 741

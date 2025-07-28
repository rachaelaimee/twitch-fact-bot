# 🚀 Deployment Guide

## Quick Start (Local Development)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/twitch-fact-bot.git
cd twitch-fact-bot
pip install -r requirements.txt
python setup.py  # Validate setup
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Twitch credentials
```

### 3. Run Bot

```bash
python main.py
```

## 🔧 Production Deployment Options

### Option A: Virtual Private Server (VPS)

**Recommended for**: Always-on bots with scheduled posting

```bash
# On your VPS (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip git screen

# Clone and setup
git clone https://github.com/yourusername/twitch-fact-bot.git
cd twitch-fact-bot
pip3 install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your credentials

# Run in background with screen
screen -S factbot
python3 main.py
# Press Ctrl+A, then D to detach
```

### Option B: Raspberry Pi

**Recommended for**: 24/7 home hosting

```bash
# Install Python 3.9+ on Raspberry Pi OS
sudo apt update
sudo apt install python3.9 python3.9-pip git

# Setup bot
git clone https://github.com/yourusername/twitch-fact-bot.git
cd twitch-fact-bot
python3.9 -m pip install -r requirements.txt

# Create systemd service for auto-start
sudo nano /etc/systemd/system/factbot.service
```

**Service file content:**

```ini
[Unit]
Description=Twitch Fact Bot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/twitch-fact-bot
ExecStart=/usr/bin/python3.9 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable service:**

```bash
sudo systemctl enable factbot.service
sudo systemctl start factbot.service
sudo systemctl status factbot.service
```

### Option C: Cloud Platforms

#### Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "worker: python main.py" > Procfile

# Deploy
heroku create your-fact-bot
heroku config:set TWITCH_TOKEN=your_token
heroku config:set TWITCH_CLIENT_ID=your_client_id
heroku config:set BOT_USERNAME=your_bot_name
heroku config:set CHANNEL_NAME=your_channel
git push heroku main
```

#### DigitalOcean App Platform

```yaml
# app.yaml
name: twitch-fact-bot
services:
  - name: bot
    source_dir: /
    github:
      repo: yourusername/twitch-fact-bot
      branch: main
    run_command: python main.py
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
      - key: TWITCH_TOKEN
        value: your_token
        type: SECRET
```

#### AWS EC2

```bash
# Launch t3.micro instance
# Connect via SSH
sudo yum update -y
sudo yum install python3 python3-pip git -y

# Setup bot
git clone https://github.com/yourusername/twitch-fact-bot.git
cd twitch-fact-bot
pip3 install -r requirements.txt

# Configure and run
cp .env.example .env
nano .env
nohup python3 main.py &
```

## 🔐 Security Best Practices

### Environment Variables

Never commit your `.env` file! Always use environment variables in production:

```bash
export TWITCH_TOKEN="oauth:your_token"
export TWITCH_CLIENT_ID="your_client_id"
export BOT_USERNAME="your_bot_name"
export CHANNEL_NAME="your_channel"
```

### Token Security

- Regenerate tokens periodically
- Use separate bot accounts for production
- Monitor bot activity regularly
- Keep your deployment server updated

## 📊 Monitoring & Maintenance

### Log Monitoring

```bash
# View real-time logs
tail -f bot.log

# Monitor system resources
htop
```

### Health Checks

```bash
# Check if bot is running
ps aux | grep python
screen -list

# Test bot responsively
curl -X GET "https://tmi.twitch.tv/group/user/your_channel/chatters"
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Restart bot (if using screen)
screen -r factbot
# Ctrl+C to stop, then restart
python3 main.py
```

## 🛠️ Troubleshooting

### Common Issues

**Bot won't connect:**

- Check internet connection
- Verify Twitch credentials
- Ensure OAuth token is valid
- Check if bot account is banned

**Commands not working:**

- Check command cooldowns
- Verify bot has send message permissions
- Look for error messages in logs

**High memory usage:**

- Restart bot periodically
- Check for memory leaks in logs
- Consider upgrading server resources

### Debug Mode

Enable detailed logging by editing `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Port and Firewall

Twitch IRC uses port 6667 (IRC) or 443 (WebSocket):

```bash
# Check if ports are open
telnet irc.chat.twitch.tv 6667
```

## 📈 Scaling Considerations

### Multiple Channels

- Modify bot configuration for multiple channels
- Consider resource usage with more channels
- Implement channel-specific fact themes

### High Traffic

- Monitor response times
- Consider rate limiting adjustments
- Scale server resources as needed

### Database Migration

For large fact collections, consider migrating from JSON to:

- SQLite (local database)
- PostgreSQL (production database)
- MongoDB (document database)

## 🔄 Backup Strategy

### Configuration Backup

```bash
# Backup configuration
tar -czf factbot-config-$(date +%Y%m%d).tar.gz data/config/ data/facts/ .env
```

### Automated Backups

```bash
# Add to crontab for daily backups
0 2 * * * cd /path/to/twitch-fact-bot && tar -czf backups/factbot-$(date +\%Y\%m\%d).tar.gz data/ .env
```

## 🆘 Support

### Getting Help

1. Check this deployment guide
2. Review the main README.md
3. Check GitHub Issues
4. Contact via GitHub or Twitch

### Reporting Issues

Include:

- Operating system and version
- Python version
- Error messages
- Bot configuration (without credentials)
- Steps to reproduce

---

**Happy Deploying!** 🚀✨

Your fact bot is ready to serve educational content 24/7!

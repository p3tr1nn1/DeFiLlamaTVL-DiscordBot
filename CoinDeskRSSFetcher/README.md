# CryptoNews-DiscordBot 🌍💬

![GitHub stars](https://img.shields.io/github/stars/p3tr1nn1/CryptoNews-DiscordBot?style=social) ![GitHub forks](https://img.shields.io/github/forks/p3tr1nn1/CryptoNews-DiscordBot?style=social) ![GitHub watchers](https://img.shields.io/github/watchers/p3tr1nn1/CryptoNews-DiscordBot?style=social) ![License](https://img.shields.io/github/license/p3tr1nn1/CryptoNews-DiscordBot)

**CryptoNews-DiscordBot** is a Python-based automation tool for crypto enthusiasts. It fetches the latest news from various cryptocurrency RSS feeds and relays this information through Discord notifications, HTML pages, and JSON files.

## 🚀 Features

- 📰 Fetches crypto news from multiple RSS feeds.
- 📄 Creates JSON files for offline processing.
- 📢 Sends updates to Discord channels.
- 🌐 Generates an HTML page with the latest news.


## 📋 Installation and Configuration

### Prerequisites

- 🐍 Python 3.x
- 📦 pip (Python package manager)
- 🗃️ SQLite3
- 🎮 Discord account for webhook setup

### 🐧 Setup on Ubuntu

1. **Clone the repository:**
   ```bash
   git clone https://github.com/p3tr1nn1/CryptoNews-DiscordBot.git
   cd CryptoNews-DiscordBot
   ```

2. **Install dependencies:**
   ```bash
   pip3 install feedparser requests
   ```

3. **Discord Webhook Setup:**
   - Navigate to your Discord server settings ➡️ 'Integrations'.
   - Click 'Create Webhook' and set your preferred channel.
   - Copy the webhook URL.

4. **Configure environment variables:**
   ```bash
   export DISCORD_WEBHOOK_URL='your_discord_webhook_url'
   ```

### 🚀 Usage

Run the main script:
```bash
python3 main.py
```

## 📜 License

Distributed under the MIT License. See `LICENSE.md` for more information.

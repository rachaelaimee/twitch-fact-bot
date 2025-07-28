# 🖤✨ Twitch Fact Bot ✨🖤

**A customizable, feature-rich Twitch chatbot for educational streamers**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![TwitchIO](https://img.shields.io/badge/TwitchIO-2.9.1-purple.svg)](https://twitchio.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A intelligent Twitch bot designed for educational content creators, featuring themed fact categories, smart randomization, and portfolio-quality code architecture.

## 🌟 Features

### 📚 Core Functionality

- **Smart Fact Distribution**: Advanced randomization that prevents immediate repeats
- **Theme-Based Categories**: Spooky/Witchy, Science, History, and Fun facts
- **Intelligent Cooldowns**: Per-user command limiting to prevent spam
- **Automatic Posting**: Scheduled fact sharing at customizable intervals

### 🎮 Interactive Commands

| Command        | Description                    | Example Output                                        |
| -------------- | ------------------------------ | ----------------------------------------------------- |
| `!fact`        | Random fact from default theme | `🖤 Spooky Fact: Ravens can remember faces...`        |
| `!factspooky`  | Witchy & Halloween facts       | `🖤 Spooky Fact: Crystal balls were used by...`       |
| `!factscience` | Scientific discoveries         | `🔬 Science Fact: Octopuses have three hearts...`     |
| `!facthistory` | Historical trivia              | `📜 History Fact: Cleopatra lived closer to...`       |
| `!factfun`     | Quirky & surprising facts      | `⭐ Fun Fact: Bubble wrap was invented as wallpaper!` |
| `!factlist`    | Available themes & shortcuts   | Shows all commands and fact counts                    |
| `!themes`      | Theme information              | Lists available categories                            |
| `!factcount`   | Statistics                     | Total facts or per-theme counts                       |

### 🔧 Advanced Features

- **Theme-Specific Prefixes**: Each category has unique branding
- **Configurable Settings**: Easy customization via INI files
- **Extensible Architecture**: JSON-based fact storage for easy updates
- **Error Handling**: Graceful degradation and user-friendly error messages
- **Professional Logging**: Comprehensive activity tracking

## 📊 Content Statistics

- **🖤 Spooky Facts**: 30 witchy, Halloween, and mysterious facts
- **🔬 Science Facts**: 30 fascinating scientific discoveries and trivia
- **📜 History Facts**: 30 interesting historical events and figures
- **⭐ Fun Facts**: 25 quirky, surprising everyday facts
- **📈 Total Content**: 115+ facts with room for infinite expansion

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- A Twitch account for your bot
- Basic terminal/command prompt knowledge

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/twitch-fact-bot.git
   cd twitch-fact-bot
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Get Twitch Credentials**

   - Create app at [Twitch Developers](https://dev.twitch.tv/console/apps)
   - Generate token at [Twitch Token Generator](https://twitchtokengenerator.com/)
   - Set OAuth Redirect URL to: `https://localhost`

4. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Customize settings**

   - Edit `data/config/bot_config.ini` for personalization
   - Modify fact prefixes, intervals, and themes

6. **Run the bot**
   ```bash
   python main.py
   ```

### Validation

Run the setup checker to verify your configuration:

```bash
python setup.py
```

## 🏗️ Architecture

### Project Structure

```
twitch-fact-bot/
├── 🤖 bot/                    # Core bot logic
│   ├── fact_manager.py        # Fact storage & retrieval
│   ├── twitch_bot.py         # Main bot class & commands
│   └── __init__.py           # Package initialization
├── 📊 data/                   # Configuration & content
│   ├── facts/                # JSON fact databases
│   │   ├── spooky.json       # Halloween & witchy facts
│   │   ├── science.json      # Scientific trivia
│   │   ├── history.json      # Historical facts
│   │   └── custom.json       # Fun & quirky facts
│   └── config/               # Bot configuration
│       ├── bot_config.ini    # Main settings
│       └── themes.json       # Theme definitions
├── 🔧 Configuration Files
│   ├── main.py              # Application entry point
│   ├── setup.py             # Setup validation tool
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment template
│   └── .gitignore          # Git ignore rules
└── 📚 Documentation
    └── README.md           # This file
```

### Design Patterns

- **Repository Pattern**: Clean separation of data access (FactManager)
- **Command Pattern**: Modular command structure with TwitchIO
- **Observer Pattern**: Event-driven message handling
- **Strategy Pattern**: Theme-specific formatting and behavior
- **Singleton Pattern**: Configuration management

## 🎨 Customization

### Adding New Facts

Edit the JSON files in `data/facts/`:

```json
{
  "theme": "spooky",
  "facts": ["Your new spooky fact here! 🖤"]
}
```

### Creating New Themes

1. Create new JSON file: `data/facts/yourtheme.json`
2. Add theme prefix to `bot_config.ini`
3. Add command in `twitch_bot.py` (optional)

### Personality Customization

Modify `data/config/bot_config.ini`:

```ini
[POSTING]
fact_prefix = 🔮 Mystical Knowledge:
spooky_prefix = 👻 Spooky Secret:
interval_minutes = 30
```

## 🔮 Perfect for Educational Streamers

This bot excels in educational streaming environments:

- **🎃 Horror/Spooky Streamers**: Rich Halloween and supernatural content
- **🔬 Science Educators**: Fascinating scientific facts and discoveries
- **📚 History Buffs**: Engaging historical trivia and events
- **🎮 General Streamers**: Universal fun facts for any audience

## 🛠️ Technical Implementation

### Key Technologies

- **TwitchIO 2.9.1**: Official Twitch IRC library
- **asyncio**: Asynchronous programming for real-time chat
- **configparser**: Flexible configuration management
- **JSON**: Human-readable data storage
- **Python 3.9+**: Modern language features

### Performance Features

- **Smart Caching**: Facts loaded once, served efficiently
- **Memory Management**: Minimal resource footprint
- **Error Recovery**: Automatic reconnection and graceful failures
- **Rate Limiting**: Built-in spam protection

## 🔧 Configuration Options

### Bot Behavior

```ini
[COMMANDS]
enable_fact_command = true    # Enable/disable !fact command
command_cooldown = 30        # Seconds between user commands
allow_theme_selection = true # Allow !fact [theme] syntax

[POSTING]
auto_post = true            # Automatic fact posting
interval_minutes = 60       # Minutes between auto-posts
default_theme = spooky      # Default fact category
```

### Theme Customization

```ini
[POSTING]
spooky_prefix = 🖤 Spooky Fact:
science_prefix = 🔬 Science Fact:
history_prefix = 📜 History Fact:
custom_prefix = ⭐ Fun Fact:
```

## 📈 Future Enhancements

- **🤖 AI Integration**: Claude/ChatGPT fact generation
- **🖥️ Web Dashboard**: Browser-based management interface
- **📊 Analytics**: Fact popularity and engagement metrics
- **🎭 Seasonal Content**: Holiday-specific fact rotations
- **👥 Community Features**: User-submitted facts with moderation
- **🔗 Platform Expansion**: Discord, YouTube, and other platforms

## 📞 Support & Contributing

### Issues & Suggestions

Found a bug or have an idea? [Open an issue](https://github.com/yourusername/twitch-fact-bot/issues)!

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Code formatting
black bot/ main.py setup.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [TwitchIO](https://twitchio.readthedocs.io/) by TwitchDev
- Inspired by educational content creators and the streaming community
- Designed for accessibility and ease of use

## 🎯 About This Project

This Twitch Fact Bot represents a portfolio-quality Python application showcasing:

- **Clean Architecture**: Modular, maintainable code structure
- **Professional Documentation**: Comprehensive README and inline docs
- **User Experience**: Intuitive commands and helpful error messages
- **Extensibility**: Easy to customize and expand functionality
- **Production Ready**: Error handling, logging, and configuration management

Perfect for demonstrating software development skills in:

- Python programming
- API integration (Twitch)
- Asynchronous programming
- Configuration management
- Data structure design
- User interface design (CLI)

---

_Built with 🖤 for the educational streaming community_

**Live Demo**: [twitch.tv/ivytenebrae](https://twitch.tv/ivytenebrae) - Try `!factspooky` in chat!

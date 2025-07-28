import asyncio
from datetime import datetime, timedelta
from twitchio.ext import commands
from twitchio import Message
import configparser
import os
from .fact_manager import FactManager

class TwitchFactBot(commands.Bot):
    """Main Twitch bot class that handles chat commands and automatic posting"""
    
    def __init__(self, config_path: str = "data/config/bot_config.ini"):
        # Load configuration
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        # Get bot settings from config
        self.channel_name = self.config.get('TWITCH', 'channel', fallback='your_channel_name')
        self.bot_username = self.config.get('TWITCH', 'bot_username', fallback='your_bot_username')
        
        # Get posting settings
        self.auto_post = self.config.getboolean('POSTING', 'auto_post', fallback=True)
        self.interval_minutes = self.config.getint('POSTING', 'interval_minutes', fallback=60)
        self.default_theme = self.config.get('POSTING', 'default_theme', fallback='spooky')
        self.fact_prefix = self.config.get('POSTING', 'fact_prefix', fallback='✨ Fact: ')
        
        # Theme-specific prefixes
        self.theme_prefixes = {
            'spooky': self.config.get('POSTING', 'spooky_prefix', fallback='🖤 Spooky Fact: '),
            'science': self.config.get('POSTING', 'science_prefix', fallback='🔬 Science Fact: '),
            'history': self.config.get('POSTING', 'history_prefix', fallback='📜 History Fact: '),
            'custom': self.config.get('POSTING', 'custom_prefix', fallback='⭐ Fun Fact: ')
        }
        
        # Get command settings
        self.enable_fact_command = self.config.getboolean('COMMANDS', 'enable_fact_command', fallback=True)
        self.command_cooldown = self.config.getint('COMMANDS', 'command_cooldown', fallback=30)
        self.allow_theme_selection = self.config.getboolean('COMMANDS', 'allow_theme_selection', fallback=True)
        
        # Initialize fact manager
        self.fact_manager = FactManager()
        
        # Cooldown tracking
        self.last_command_time = {}
        self.last_auto_post = datetime.now()
        
        # Get OAuth token from environment
        token = os.getenv('TWITCH_TOKEN')
        if not token:
            raise ValueError("TWITCH_TOKEN environment variable not found! Please check your .env file.")
        
        # Initialize the bot
        super().__init__(
            token=token,
            prefix='!',
            initial_channels=[self.channel_name],
            nick=self.bot_username
        )
        
        print(f"🤖 Bot initialized for channel: {self.channel_name}")
        print(f"📚 Loaded themes: {', '.join(self.fact_manager.get_available_themes())}")
    
    async def event_ready(self):
        """Called when bot is connected and ready"""
        print(f'🔮 {self.nick} is ready and connected to #{self.channel_name}!')
        print(f'⚡ Auto-posting: {"Enabled" if self.auto_post else "Disabled"}')
        
        # Start auto-posting if enabled
        if self.auto_post:
            asyncio.create_task(self.auto_post_facts())
    
    async def event_message(self, message: Message):
        """Handle incoming chat messages"""
        # Ignore messages from the bot itself
        if message.echo:
            return
        
        # Process commands
        await self.handle_commands(message)
    
    @commands.command(name='fact')
    async def fact_command(self, ctx: commands.Context, *, theme: str = None):
        """Handle the !fact command"""
        if not self.enable_fact_command:
            return
        
        # Check cooldown
        user_id = ctx.author.name
        now = datetime.now()
        
        if user_id in self.last_command_time:
            time_since_last = now - self.last_command_time[user_id]
            if time_since_last.total_seconds() < self.command_cooldown:
                remaining = self.command_cooldown - int(time_since_last.total_seconds())
                await ctx.send(f"@{user_id} Please wait {remaining} more seconds before using !fact again! ⏰")
                return
        
        self.last_command_time[user_id] = now
        
        # Handle theme selection
        if theme and not self.allow_theme_selection:
            theme = None  # Ignore theme if not allowed
        
        if not theme:
            theme = self.default_theme
        
        # Get fact from fact manager
        fact = self.fact_manager.get_random_fact(theme)
        
        # Use theme-specific prefix if available, otherwise use default
        prefix = self.theme_prefixes.get(theme, self.fact_prefix)
        formatted_fact = f"{prefix}{fact}"
        await ctx.send(formatted_fact)
        
        print(f"📤 Sent fact to {ctx.author.name}: {theme} theme")
    
    @commands.command(name='themes')
    async def themes_command(self, ctx: commands.Context):
        """Show available fact themes"""
        themes = self.fact_manager.get_available_themes()
        theme_list = ", ".join(themes)
        
        await ctx.send(f"Available fact themes: {theme_list} 📚 Use !fact [theme] to get a specific type!")
    
    @commands.command(name='factcount')
    async def factcount_command(self, ctx: commands.Context, *, theme: str = None):
        """Show how many facts are available"""
        if theme:
            count = self.fact_manager.get_theme_fact_count(theme)
            if count > 0:
                await ctx.send(f"Theme '{theme}' has {count} facts available! 📊")
            else:
                await ctx.send(f"Theme '{theme}' not found or has no facts! 🤔")
        else:
            total = sum(self.fact_manager.get_theme_fact_count(t) for t in self.fact_manager.get_available_themes())
            await ctx.send(f"Total facts available: {total} across all themes! 🎯")
    
    # Shortcut commands for specific themes
    @commands.command(name='factspooky')
    async def factspooky_command(self, ctx: commands.Context):
        """Get a spooky/witchy fact"""
        await self._send_themed_fact(ctx, 'spooky')
    
    @commands.command(name='factscience')
    async def factscience_command(self, ctx: commands.Context):
        """Get a science fact"""
        await self._send_themed_fact(ctx, 'science')
    
    @commands.command(name='facthistory')
    async def facthistory_command(self, ctx: commands.Context):
        """Get a history fact"""
        await self._send_themed_fact(ctx, 'history')
    
    @commands.command(name='factfun')
    async def factfun_command(self, ctx: commands.Context):
        """Get a fun fact"""
        await self._send_themed_fact(ctx, 'custom')
    
    @commands.command(name='factlist')
    async def factlist_command(self, ctx: commands.Context):
        """Show all available fact themes and shortcuts"""
        themes = self.fact_manager.get_available_themes()
        
        theme_info = []
        for theme in themes:
            count = self.fact_manager.get_theme_fact_count(theme)
            theme_info.append(f"{theme} ({count} facts)")
        
        shortcuts = "!factspooky, !factscience, !facthistory, !factfun"
        
        await ctx.send(f"📚 Available themes: {', '.join(theme_info)} | Shortcuts: {shortcuts} | Use !fact [theme] or shortcuts! ✨")
    
    async def _send_themed_fact(self, ctx: commands.Context, theme: str):
        """Helper method to send a fact from a specific theme with cooldown check"""
        if not self.enable_fact_command:
            return
        
        # Check cooldown
        user_id = ctx.author.name
        now = datetime.now()
        
        if user_id in self.last_command_time:
            time_since_last = now - self.last_command_time[user_id]
            if time_since_last.total_seconds() < self.command_cooldown:
                remaining = self.command_cooldown - int(time_since_last.total_seconds())
                await ctx.send(f"@{user_id} Please wait {remaining} more seconds before using fact commands again! ⏰")
                return
        
        self.last_command_time[user_id] = now
        
        # Get fact from fact manager
        fact = self.fact_manager.get_random_fact(theme)
        
        # Use theme-specific prefix if available, otherwise use default
        prefix = self.theme_prefixes.get(theme, self.fact_prefix)
        formatted_fact = f"{prefix}{fact}"
        await ctx.send(formatted_fact)
        
        print(f"📤 Sent fact to {ctx.author.name}: {theme} theme")
    
    async def auto_post_facts(self):
        """Automatically post facts at intervals"""
        while True:
            try:
                # Wait for the specified interval
                await asyncio.sleep(self.interval_minutes * 60)
                
                # Get a random fact using default theme
                fact = self.fact_manager.get_random_fact(self.default_theme)
                formatted_fact = f"{self.fact_prefix}{fact}"
                
                # Post to the channel
                channel = self.get_channel(self.channel_name)
                if channel:
                    await channel.send(formatted_fact)
                    print(f"🕐 Auto-posted fact: {self.default_theme} theme")
                
                self.last_auto_post = datetime.now()
                
            except Exception as e:
                print(f"Error in auto-posting: {e}")
                # Wait a bit before trying again
                await asyncio.sleep(60) 
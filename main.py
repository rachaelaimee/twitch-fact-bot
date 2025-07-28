#!/usr/bin/env python3
"""
🖤✨ Twitch Fact Bot ✨🖤
A customizable bot for posting themed facts in Twitch chat!

Perfect for spooky streamers, witchy vibes, and educational content.
"""

import os
import asyncio
from dotenv import load_dotenv
from bot.twitch_bot import TwitchFactBot

def main():
    """Main function to start the Twitch fact bot"""
    
    print("🖤✨ Starting Twitch Fact Bot ✨🖤")
    print("=" * 40)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ['TWITCH_TOKEN', 'BOT_USERNAME', 'CHANNEL_NAME']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please check your .env file and make sure these are set!")
        print("📖 See the setup guide for help getting your Twitch credentials.")
        return
    
    try:
        # Create and run the bot
        bot = TwitchFactBot()
        print("🚀 Starting bot connection...")
        bot.run()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Check your configuration and try again!")

if __name__ == "__main__":
    main() 
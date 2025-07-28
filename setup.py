#!/usr/bin/env python3
"""
Quick setup script for Twitch Fact Bot
Helps validate your setup and get you started!
"""

import os
import json

def main():
    print("🖤✨ Twitch Fact Bot Setup Helper ✨🖤")
    print("=" * 45)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ No .env file found!")
        print("💡 Copy .env.example to .env and fill in your Twitch credentials.")
        
        # Offer to create .env from example
        if os.path.exists('.env.example'):
            create = input("🤔 Would you like me to create .env from the example? (y/n): ")
            if create.lower() == 'y':
                import shutil
                shutil.copy('.env.example', '.env')
                print("✅ Created .env file! Now edit it with your credentials.")
        return
    else:
        print("✅ .env file found!")
    
    # Check if basic directories exist
    required_dirs = ['bot', 'data/facts', 'data/config']
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
    
    # Check fact files
    fact_files = ['spooky.json', 'science.json', 'history.json', 'custom.json']
    print("\n📚 Checking fact files:")
    
    total_facts = 0
    for filename in fact_files:
        file_path = os.path.join('data/facts', filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    fact_count = len(data.get('facts', []))
                    total_facts += fact_count
                    print(f"✅ {filename}: {fact_count} facts")
            except Exception as e:
                print(f"❌ {filename}: Error reading file - {e}")
        else:
            print(f"❌ {filename}: File not found")
    
    print(f"\n🎯 Total facts available: {total_facts}")
    
    # Check config file
    config_path = 'data/config/bot_config.ini'
    if os.path.exists(config_path):
        print("✅ Bot configuration file found!")
        print("💡 Edit data/config/bot_config.ini to customize your bot settings.")
    else:
        print("❌ Bot configuration file missing!")
    
    print("\n🚀 Next steps:")
    print("1. Make sure your .env file has your Twitch credentials")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python main.py")
    print("4. Test with !fact in your Twitch chat")
    
    print("\n🖤✨ Happy streaming! ✨🖤")

if __name__ == "__main__":
    main() 
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from database import init_db

# Load environment variables
load_dotenv()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await bot.change_presence(activity=discord.Game(name="Leaderboards & Curses"))
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def load_cogs():
    """Load all cogs from the cogs directory"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename}")

async def main():
    """Start the bot"""
    # Initialize database
    init_db()
    
    # Load cogs
    async with bot:
        await load_cogs()
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("DISCORD_TOKEN not found in .env file!")
        await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

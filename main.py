import discord
from discord.ext import commands
import os
from keep_alive import server_on
from send_clip import send_clip
from video_menu import menu
from show_menu_button import show_menu_button

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Start Flask server (for Render)
server_on()

# Register commands
bot.command(name="ส่งคลิป")(send_clip)
bot.command(name="เมนู")(menu)
bot.command(name="แสดงปุ่มเมนู")(show_menu_button)

@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์: {bot.user}")

bot.run(TOKEN)

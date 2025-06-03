import discord
from discord.ext import commands
import gdown
import os
import asyncio
import time

CHANNEL_ID = 1379036193525862460       #!ส่งคลิป [ชื่อเรื่อง]
LOG_CHANNEL_ID = 1378977947054247957
COUNTDOWN_TIME = 10

VIDEOS = {
    "กังฟูแพนด้า": "19p7U285U5KVkY-rHqq8QmApOzxdvc2aE",
    "ไอรอนแมน": "1tc4CwafrbcGHobe5WsVkuSX2jVqP9qxz",
    "เดดพูล": "1ru539tzbxOSe8vkQO677GsyeZBuOwW_a"
}

user_processing = set()

class DeliveryChoice(discord.ui.View):
    def __init__(self, file_name, title, ctx):
        super().__init__(timeout=60)
        self.file_name = file_name
        self.title = title
        self.ctx = ctx

    @discord.ui.button(label="📤 ส่งในกลุ่ม", style=discord.ButtonStyle.primary)
    async def send_to_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                f"❌ ปุ่มนี้สามารถใช้งานได้โดย **{self.ctx.author.display_name}** เท่านั้น", ephemeral=True)
            return
        await interaction.response.defer()
        video_channel = self.ctx.bot.get_channel(CHANNEL_ID)
        await video_channel.send(f"🎬 เรื่อง: **{self.title}**", file=discord.File(self.file_name))
        await self.log("กลุ่ม")
        await interaction.followup.send("✅ ส่งในกลุ่มเรียบร้อยแล้ว", ephemeral=True)
        self.cleanup()

    @discord.ui.button(label="📩 ส่งทาง DM", style=discord.ButtonStyle.secondary)
    async def send_to_dm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                f"❌ ปุ่มนี้สามารถใช้งานได้โดย **{self.ctx.author.display_name}** เท่านั้น", ephemeral=True)
            return
        await interaction.response.defer()
        try:
            await interaction.user.send(f"🎬 เรื่อง: **{self.title}**", file=discord.File(self.file_name))
            await self.log("DM")
            await interaction.followup.send("✅ ส่งทาง DM แล้ว!", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ ไม่สามารถส่ง DM ได้", ephemeral=True)
        self.cleanup()

    def cleanup(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        self.stop()

    async def log(self, method):
        log_channel = self.ctx.bot.get_channel(LOG_CHANNEL_ID)
        await log_channel.send(f"👀 **{self.ctx.author.display_name}** กำลังดูเรื่อง **{self.title}** ทาง {method}")

async def send_clip(ctx, *, title: str = None):
    if ctx.author.id in user_processing:
        await ctx.send("⏳ กรุณารอให้ส่งคลิปก่อนหน้าสำเร็จก่อน แล้วค่อยลองใหม่")
        return

    user_processing.add(ctx.author.id)
    try:
        if not title or title.strip() not in VIDEOS:
            await ctx.send(f"❌ ไม่พบชื่อเรื่อง หรือไม่ได้ระบุชื่อ\n📽 เรื่องที่มีให้: {' | '.join(VIDEOS.keys())}")
            return

        title = title.strip()
        msg = await ctx.send(f"⏳ กำลังเตรียมส่ง **{title}**...")
        url = f"https://drive.google.com/uc?id={VIDEOS[title]}"
        file_name = "video.mp4"
        gdown.download(url, file_name, quiet=False)

        for i in range(COUNTDOWN_TIME, 0, -1):
            await msg.edit(content=f"⏳ กำลังส่ง **{title}** ใน {i} วินาที...")
            await asyncio.sleep(1)
        await msg.delete()

        await ctx.send(f"📌 ต้องการให้ส่งคลิป **{title}** ทางไหน?", view=DeliveryChoice(file_name, title, ctx))
    finally:
        user_processing.discard(ctx.author.id)

import discord
from discord.ext import commands    #!แสดงปุ่มเมนู
from video_menu import MenuView

TARGET_CHANNEL_ID = 1379036193525862460     #ใส่ ID ห้องที่ต้องการใช้งานโค๊ดนี้

class MenuTrigger(discord.ui.View):
    @discord.ui.button(label="📋 เปิดเมนูวิดีโอ", style=discord.ButtonStyle.success)
    async def menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
        if channel:
            await channel.send("📋 กรุณาเลือกชื่อเรื่องที่ต้องการ:", view=MenuView(interaction))
            await interaction.followup.send("✅ เปิดเมนูในห้องที่กำหนดแล้ว", ephemeral=True)
        else:
            await interaction.followup.send("❌ ไม่พบห้องที่กำหนด", ephemeral=True)

async def show_menu_button(ctx):
    channel = ctx.bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🎬 เมนูวิดีโอฟรี",
            description="กดปุ่มด้านล่างเพื่อเปิดเมนูเลือกวิดีโอ",
            color=discord.Color.green()
        )
        await channel.send(embed=embed, view=MenuTrigger())
        await ctx.send("✅ ส่งปุ่มเมนูไปยังห้องเรียบร้อยแล้ว")
    else:
        await ctx.send("❌ ไม่พบห้องเป้าหมาย")

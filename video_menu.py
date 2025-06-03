import discord
from discord.ext import commands

TARGET_CHANNEL_ID = 1379036193525862460   #!เมนู

VIDEOS = {
    "กังฟูแพนด้า": "",
    "ไอรอนแมน": "",
    "เดดพูล": ""
}

class MenuView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.used = False
        for title in VIDEOS.keys():
            self.add_item(MenuButton(title, ctx, self))

class MenuButton(discord.ui.Button):
    def __init__(self, title, ctx, view):
        super().__init__(label=title, style=discord.ButtonStyle.primary)
        self.title = title
        self.ctx = ctx
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                f"❌ เมนูนี้สร้างโดย **{self.ctx.author.display_name}** เท่านั้น", ephemeral=True)
            return
        if self.parent_view.used:
            await interaction.response.send_message("⚠️ เลือกได้เพียง 1 ครั้ง", ephemeral=True)
            return

        self.parent_view.used = True
        await interaction.response.defer()
        await self.ctx.invoke(self.ctx.bot.get_command("ส่งคลิป"), title=self.title)

        for child in self.parent_view.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        await interaction.message.edit(view=self.parent_view)
        self.parent_view.stop()

async def menu(ctx):
    if ctx.channel.id != TARGET_CHANNEL_ID:
        await ctx.send("❌ คำสั่งนี้ใช้ได้เฉพาะในห้องที่กำหนดเท่านั้น")
        return
    await ctx.send("📋 กรุณาเลือกชื่อเรื่องที่ต้องการ:", view=MenuView(ctx))

from discord.ext import commands
import discord

class AboutCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.VERSION = "1.0.0"
        print("init -> AboutCog")

    @commands.hybrid_command(name="about", description="Botについての情報を表示")
    async def about(self, ctx: commands.Context):
        await ctx.reply(embed=
                        discord.Embed(title="UniBotの情報", description="UniProjectで作成されたBotです。", color=discord.Color.blue()).add_field(name="バージョン", value=self.VERSION, inline=False), 
                        view=discord.ui.View(timeout=None).add_item(discord.ui.Button(label="レポジトリ", url="https://github.com/SharkBot-Dev/UniBot-Python")))

async def setup(bot):
    await bot.add_cog(AboutCog(bot))
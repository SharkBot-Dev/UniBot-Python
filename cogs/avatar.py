from discord.ext import commands
import discord

class AvatarCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("init -> AvatarCog")

    @commands.hybrid_command(name="avatar", description="アイコンのURLを取得")
    async def avatar(self, ctx: commands.Context, target: discord.User = None):
        user = target if target else ctx.author
        await ctx.reply(embed=discord.Embed(title=f"{user.name}のアバター", color=discord.Color.green()).set_image(url=user.display_avatar.url), view=discord.ui.View(timeout=None).add_item(discord.ui.Button(label="ダウンロード", url=user.display_avatar.url)))

async def setup(bot):
    await bot.add_cog(AvatarCog(bot))
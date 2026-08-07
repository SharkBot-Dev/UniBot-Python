from discord.ext import commands
import discord

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("init -> AdminCog")

    @commands.command(name="reload", description="cogをリロード")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog_name: str):
        await self.bot.reload_extension("cogs." + cog_name)
        await ctx.reply("リロード完了。")

    @commands.command(name="load", description="cogをロード")
    @commands.is_owner()
    async def load(self, ctx: commands.Context, cog_name: str):
        await self.bot.load_extension("cogs." + cog_name)
        await ctx.reply("ロード完了。")

    @commands.command(name="sync", description="スラッシュコマンドを同期")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, cog_name: str):
        await self.bot.tree.sync()
        await ctx.reply("SyncOK！")
        
async def setup(bot):
    await bot.add_cog(AdminCog(bot))
from discord.app_commands.tree import CommandTree
from discord.ext import commands, tasks
import discord
from discord.ext.commands.bot import _default
from discord.utils import MISSING
import dotenv
import os
import aiosqlite

dotenv.load_dotenv()

intents = discord.Intents.none()
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.guilds = True

class UniBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="u!", intents=intents, help_command=None, chunk_guilds_at_startup=False, member_cache_flags=discord.MemberCacheFlags.none(), max_messages=0)

        self.db: aiosqlite.Connection = None
        self.cursor: aiosqlite.Cursor = None

    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("不明なコマンドです。\n`/`と入力してコマンドを確認してください。")
            return
        elif isinstance(error, commands.NotOwner):
            await ctx.reply("403 Forbidden")
            return
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"コマンドの使い方が間違っています。\n`/{ctx.command.qualified_name}`と入力してコマンドを確認してください。", allowed_mentions=discord.AllowedMentions.none())
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"コマンドの使い方が間違っています。\n`/{ctx.command.qualified_name}`と入力してコマンドを確認してください。", allowed_mentions=discord.AllowedMentions.none())
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("403 Forbidden")
            return
        else:
            await ctx.reply(embed=discord.Embed(title="すみません。エラーが発生しました。", color=discord.Color.red(), description=f"```{error}```"))

    async def setup_hook(self):
        self.db = await aiosqlite.connect("settings.db")
        self.cursor = await self.db.cursor()

        # DBのセットアップ
        await self.cursor.execute("CREATE TABLE IF NOT EXISTS pin(id INTEGER PRIMARY KEY, guild_id TEXT, channel_id TEXT, message_id TEXT, text TEXT);")

        await self.load_extension("cogs.admin")
        await self.load_extension("cogs.about")
        await self.load_extension("cogs.avatar")
        await self.load_extension("cogs.ping")
        await self.load_extension("cogs.pin")
        # await self.tree.sync()

bot = UniBot()

@tasks.loop(seconds=10)
async def loop_status():
    await bot.change_presence(activity=discord.CustomActivity(name="UniPro製Bot"))

@bot.event
async def on_ready():
    loop_status.start()
    print("Ready.")

bot.run(os.environ.get('TOKEN'))
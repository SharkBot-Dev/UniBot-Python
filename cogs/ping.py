from discord.ext import commands
import discord
import time
import asyncio

class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("init -> PingCog")

    @commands.hybrid_command(name="ping", description="Ping!")
    async def ping(self, ctx: commands.Context):
        discord_api_start_time = time.perf_counter()
        if not ctx.interaction:
            message = await ctx.send(
                embed=discord.Embed(description="計測中です..", color=discord.Color.blue())
            )
            asyncio.create_task(message.delete())
        else:
            await ctx.defer()
        discord_api_end_time = time.perf_counter()

        discord_latency_ms = (discord_api_end_time - discord_api_start_time) * 1000
        ws_latency_ms = self.bot.latency * 1000

        api_text = f"{discord_latency_ms:.2f} ms"
        ws_text = f"{ws_latency_ms:.2f} ms"

        await ctx.reply(embed=discord.Embed(title="Ping", description="Pong!", color=discord.Color.blue()).add_field(name="WebSocket", value=ws_text, inline=True).add_field(name="コマンド受信", value=api_text, inline=True))

async def setup(bot):
    await bot.add_cog(PingCog(bot))
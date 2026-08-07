from discord.ext import commands
import discord
import time

from discord.utils import MISSING

class PinModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="メッセージのピン留め", timeout=180)

        self.text = discord.ui.TextInput(label="投稿内容", style=discord.TextStyle.long, placeholder="投稿内容を入力してください。すでにPinされたメッセージがある場合は上書きされます。")
        self.add_item(self.text)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            message = await interaction.channel.send(embed=discord.Embed(description=self.text.value, color=discord.Color.green()).set_footer(text="Pinned Message"))
        except Exception as e:
            await interaction.followup.send(content="このチャンネルではメッセージを送信できません。", ephemeral=True)
            return

        await interaction.client.cursor.execute("DELETE FROM pin WHERE channel_id = ?", (str(interaction.channel_id),))
        await interaction.client.cursor.execute("INSERT INTO pin (guild_id, channel_id, message_id, text) VALUES (?, ?, ?, ?)", (str(interaction.guild_id), str(interaction.channel_id), str(message.id), self.text.value,))

        await interaction.client.db.commit()

        await interaction.followup.send(ephemeral=True, content="メッセージをピン留めしました。")
        return

class PinCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.working = set()
        print("init -> PinCog")

    @commands.hybrid_command(name="pin", description="メッセージをピン留めします。")
    @commands.has_permissions(pin_messages=True)
    async def pin(self, ctx: commands.Context):
        if not ctx.interaction.response:
            await ctx.reply("`/pin`で実行できます。")
            return
        await ctx.interaction.response.send_modal(PinModal())

    @commands.hybrid_command(name="unpin", description="ピン留めを解除します。")
    @commands.has_permissions(pin_messages=True)
    async def unpin(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute('SELECT message_id, text FROM pin WHERE channel_id = ?', (str(ctx.channel.id),))
        data = await self.bot.cursor.fetchone()
        if not data:
            await ctx.reply(content="このチャンネルにはピン留めされたメッセージがありません。", ephemeral=True)
            return

        try:
            await discord.PartialMessage(
                channel=ctx.channel, id=int(data[0])
            ).delete()
        except discord.HTTPException:
            pass

        await self.bot.cursor.execute(
            "DELETE FROM pin WHERE channel_id = ?", (str(ctx.channel.id),)
        )
        await self.bot.db.commit()

        await ctx.reply(embed=discord.Embed(title="ピン留めを解除しました", color=discord.Color.green()), ephemeral=True)

    @commands.Cog.listener("on_message")
    async def on_message_pin(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.guild:
            return

        await self.bot.cursor.execute('SELECT guild_id, channel_id, message_id, text FROM pin WHERE channel_id = ?', (str(message.channel.id),))
        data = await self.bot.cursor.fetchone()
        if not data:
            return

        try:

            if message.channel.id in self.working:
                return

            self.working.add(message.channel.id)

            try:
                await discord.PartialMessage(channel=message.channel, id=int(data[2])).delete()
            except:
                return
            new_message = await message.channel.send(embed=discord.Embed(description=data[3], color=discord.Color.green()).set_footer(text="Pinned Message"))

            await self.bot.cursor.execute('UPDATE pin SET message_id = ? WHERE channel_id = ?', (str(new_message.id), str(message.channel.id)),)
            await self.bot.db.commit()


        finally:
            self.working.remove(message.channel.id)
        
async def setup(bot):
    await bot.add_cog(PinCog(bot))
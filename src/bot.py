from constants import STREAM_TRACK_IDS, GENERAL_CHANNEL, GUILDS
from responses import handle_bili_response, handle_custom_responses, create_bili_response
import discord
from discord.ext import commands
import os


DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


def run_ben_xu_bot():
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        # for gid in GUILDS:
        #     await bot.tree.sync(guild=discord.Object(id=gid))
        await bot.tree.sync(guild=discord.Object(id=GUILDS[1]))
        print("{} is now running!".format(bot.user))

    @bot.event
    async def on_message(message):
        # avoid infinite response loop
        if message.author == bot.user:
            return

        speaker = str(message.author)
        u_message = str(message.content)
        channel_id = message.channel.id

        if u_message.startswith("!bili"):
            create_resp = await create_bili_response(u_message, speaker, channel_id)
            await message.channel.send(create_resp)
            return
        bili_resp = await handle_bili_response(u_message, speaker, channel_id)
        if bili_resp:
            await message.channel.send(bili_resp)
        else:
            custom_resp = await handle_custom_responses(u_message, speaker, channel_id)
            if custom_resp:
                await message.channel.send(custom_resp)

    @bot.event
    async def on_voice_state_update(member, before, after):
        is_target = str(member.id) in STREAM_TRACK_IDS
        is_new_stream = not before.self_stream and after.self_stream
        if is_target and is_new_stream:
            stream_msg = "@everyone: {} has started streaming!".format(member.name)
            await bot.get_channel(GENERAL_CHANNEL).send(stream_msg)

    @bot.tree.command(name="hello", description="让大B老师开口说话！")
    async def hello(interaction: discord.Interaction):
        print("command received!")
        await interaction.response.send_message("command received!")

    bot.run(DISCORD_TOKEN)

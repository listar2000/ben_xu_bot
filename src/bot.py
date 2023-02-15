from constants import BILI_TRIGGER_WORDS, BILI_PRAISE_WORDS, STREAM_TRACK_IDS, GENERAL_CHANNEL
from dotenv import load_dotenv
import discord
import os
import re

load_dotenv("../.env")

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


def handle_bili_response(message: str, target: str) -> str:
    message = message.lower()
    pattern_trigger = re.compile('|'.join(BILI_TRIGGER_WORDS))
    pattern_praise = re.compile('|'.join(BILI_PRAISE_WORDS))

    match_trigger = re.search(pattern_trigger, message)
    match_praise = re.search(pattern_praise, message)

    target_name = target.split("#")[0]
    if match_trigger:
        trigger = match_trigger.group(0)
        print("trigger word: {} spotted".format(trigger))
        return "说什么呢！{}你个小黄金也配叫我{}？".format(target_name, trigger)
    elif match_praise:
        praise = match_praise.group(0)
        print("praise word: {} spotted".format(praise))
        return "可以可以，基操勿6。等我抽根华子马上带{}上白金".format(target_name)


def run_ben_xu_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("{} is now running!".format(client.user))

    @client.event
    async def on_message(message):
        # avoid infinite response loop
        if message.author == client.user:
            return

        speaker = str(message.author)
        u_message = str(message.content)

        response = handle_bili_response(u_message, speaker)
        if response:
            await message.channel.send(response)

    @client.event
    async def on_voice_state_update(member, before, after):
        is_target = str(member.id) in STREAM_TRACK_IDS
        is_new_stream = not before.self_stream and after.self_stream
        if is_target and is_new_stream:
            stream_msg = "@everyone: {} has started streaming!".format(member.name)
            await client.get_channel(GENERAL_CHANNEL).send(stream_msg)

    @client.event
    async def on_member_update(before, after):
        print(before.id, type(before.id))

    client.run(DISCORD_TOKEN)

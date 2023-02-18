import re
import time
from constants import  BILI_PRAISE_WORDS, BILI_TRIGGER_WORDS, GIST_IDS
from gist_io import load_data_from_gist, update_data_to_gist
from functools import wraps

# at most 5 messages per hour per channel
RATE_LIMIT = 5
RATE_LIMIT_PERIOD = 3600

# dicts for channel
last_reset_times, rate_counts = dict(), dict()


def rate_limit(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        channel = args[2]
        curr_time = time.time()
        if channel not in last_reset_times or curr_time - last_reset_times[channel] >= RATE_LIMIT_PERIOD:
            print("resetting the count for channel:{}".format(channel))
            last_reset_times[channel] = curr_time
            rate_counts[channel] = 0
        if rate_counts[channel] == RATE_LIMIT:
            rate_counts[channel] += 1
            return "你他妈的话太多了，劳资🚬去了"
        elif rate_counts[channel] > RATE_LIMIT:
            return ""
        else:
            res = await func(*args, **kwargs)
            if res:
                rate_counts[channel] += 1
            return res
    return inner


@rate_limit
async def handle_bili_response(message: str, target: str, channel: int) -> str:
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


@rate_limit
async def handle_custom_responses(message: str, target: str, channel: int) -> str:
    gist_name = "trigger_words.json"
    gist_id = GIST_IDS["trigger_words.json"]
    trigger_objs = await load_data_from_gist(gist_name, gist_id)
    hint_str = " \n [这是一条自动回复，通过 !bili 创建你的自动回复]"
    for trigger_obj in trigger_objs:
        keywords = trigger_obj["keywords"]
        pattern = re.compile('|'.join(keywords))
        match_trigger = re.search(pattern, message)
        if match_trigger:
            trigger = match_trigger.group(0)
            print("custom word: {} spotted".format(trigger))
            return trigger_obj["value"] + hint_str


async def create_bili_response(command: str, creator: str, channel: int) -> str:
    bili_hint = """
    🐷🐷🐷
    请使用以下语法通过!bili创建自定义回复
    例子: !bili 伊利斯/盲僧/巨魔 都是我大B的拿手英雄！
    将会创建三个关键词，对应语句"都是我大B的拿手英雄！"
    关键词/对应语句不能包含空格
    """
    bili_max = "🐷：阔咪呐赛，目前测试阶段自定义语句已满"
    bili_success = """
    🐷🐷🐷
    成功创建{}个关键词：{}
    对应语句:{}
    """
    bili_fail = """
    🐷🐷🐷
    由于网络原因，创建失败，阔咪呐赛！
    """
    substrings = command.split()
    if len(substrings) != 3 or substrings[0] != "!bili":
        return bili_hint
    else:
        gist_name = "trigger_words.json"
        gist_id = GIST_IDS[gist_name]
        old_kws = await load_data_from_gist(gist_name, gist_id)

        if len(old_kws) > 10:
            return bili_max

        new_kws = [k for k in substrings[1].split("/") if k]

        old_kws.append({
            "keywords": new_kws,
            "value": substrings[2]
        })

        if await update_data_to_gist(gist_name, gist_id, old_kws):
            return bili_success.format(len(new_kws), new_kws, substrings[2])
        else:
            return bili_fail



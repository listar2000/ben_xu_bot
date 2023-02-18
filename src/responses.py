import re
import time
from constants import  BILI_PRAISE_WORDS, BILI_TRIGGER_WORDS

# at most 5 messages per hour per channel
RATE_LIMIT = 5
RATE_LIMIT_PERIOD = 3600

# dicts for channel
last_reset_times, rate_counts = dict(), dict()


def handle_bili_response(message: str, target: str, channel: int) -> str:
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

    message = message.lower()
    pattern_trigger = re.compile('|'.join(BILI_TRIGGER_WORDS))
    pattern_praise = re.compile('|'.join(BILI_PRAISE_WORDS))

    match_trigger = re.search(pattern_trigger, message)
    match_praise = re.search(pattern_praise, message)

    target_name = target.split("#")[0]
    if match_trigger:
        trigger = match_trigger.group(0)
        print("trigger word: {} spotted".format(trigger))
        rate_counts[channel] += 1
        return "说什么呢！{}你个小黄金也配叫我{}？".format(target_name, trigger)
    elif match_praise:
        praise = match_praise.group(0)
        print("praise word: {} spotted".format(praise))
        rate_counts[channel] += 1
        return "可以可以，基操勿6。等我抽根华子马上带{}上白金".format(target_name)
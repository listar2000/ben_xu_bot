import asyncio
import json
import aiohttp
import requests

# GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_TOKEN = "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"


def _get_header():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    return headers


async def load_data_from_gist(gist_name: str, gist_id: str):
    url = f"https://api.github.com/gists/{gist_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                js = await resp.json()
                data = json.loads(js["files"][gist_name]["content"])
                return data
            else:
                print(f"request fails: {await resp.text()}")
                return None


async def update_data_to_gist(gist_name: str, gist_id: str, new_content):
    url = f"https://api.github.com/gists/{gist_id}"

    payload = {
        "files": {
            gist_name: {
                "content": json.dumps(new_content)
            }
        }
    }

    # async with aiohttp.ClientSession() as session:
    #     async with session.patch(url, headers=_get_header(), json=payload) as resp:
    #         if resp.status == 200:
    #             print("write data to Gist!")
    #             return True
    #         else:
    #             print(f"writing fails: {await resp.text()}")
    #             return False
    resp = requests.patch(url, headers=_get_header(), data=json.dumps(payload))
    if resp.status_code == 200:
        print("write data to Gist!")
        return True
    else:
        print(f"writing fails: {resp.text}")
        return False

# from constants import GIST_IDS
# gist_name = "trigger_words.json"
# gist_id = GIST_IDS[gist_name]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(update_data_to_gist(gist_name, gist_id, ["a", "b", "c"]))
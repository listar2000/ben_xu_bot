from dotenv import load_dotenv

if __name__ == "__main__":
    assert load_dotenv()

    from bot import run_ben_xu_bot
    run_ben_xu_bot()
import logging
import os
import signal
import sys

from commands import *
from signalbot import SignalBot

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


def terminate(signal, frame):
    print("Exiting...")
    sys.exit(0)


def main():
    bot_phone = os.environ["BOT_PHONE"]
    self_phone = os.environ["SELF_PHONE"]
    group_id = os.environ["GROUP_ID"]
    group_secret = os.environ["GROUP_SECRET"]

    signal_service = os.environ["SIGNAL_SERVICE"]

    config = {
        "signal_service": signal_service,
        "phone_number": bot_phone,
        "storage": None,
    }

    bot = SignalBot(config)
    bot.listen(group_id, group_secret)
    bot.listen(self_phone)

    bot.register(ChatCommand())
    bot.register(LyricsCommand())

    bot.start()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)
    main()

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
    signal_service = os.environ["SIGNAL_SERVICE"]

    config = {
        "phone_number": bot_phone,
        "signal_service": signal_service,
        "storage": None,
    }
    bot = SignalBot(config)

    if self_phone:
        bot.listen(self_phone)
    if group_id:
        bot.listen(group_id)

    bot.register(ChatCommand())
    bot.register(LyricsCommand())

    bot.start()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)
    main()

import os

from brain.interaction.received_message import RecievedMessage
from brain.interaction.phrasing import Phrasing
from signalbot import Command, Context


class ChatCommand(Command):
    def describe(self) -> str:
        return "Provide pseudo-intelligent responses based on message triggers"

    async def handle(self, c: Context):
        msg = RecievedMessage(c.message.text.casefold())
        if not msg.botname_mentioned:
            return

        response = Phrasing(msg.text, msg.trigger_type, msg.trigger_phrase, c)
        await response.send()

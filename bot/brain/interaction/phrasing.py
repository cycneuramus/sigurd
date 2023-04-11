from brain.interaction.response import Response
from brain.skills import random_lyrics
from signalbot import Context


class Phrasing:
    def __init__(
        self, msg_recieved: str, trigger_type: str, trigger_phrase: str, c: Context
    ):
        self.trigger_type = trigger_type
        self.trigger_phrase = trigger_phrase
        self.msg_recieved = msg_recieved
        self.c = c

        self.response = self._create()

    def _lyrics(self) -> str:
        artist = self.msg_recieved.split(self.trigger_phrase, 1)[1]
        return random_lyrics.get_lyrics(artist)

    def _praise(self) -> str:
        return Response("on_praise").get_fresh()

    def _blame(self) -> str:
        return Response("on_blame").get_fresh()

    def _unknown(self) -> str:
        return Response("on_unknown").get_fresh()

    async def send(self):
        await self.c.send(self.response)

    def _create(self) -> str:
        response = {
            "blame": self._blame,
            "lyrics": self._lyrics,
            "praise": self._praise,
            "": self._unknown,
        }

        return response[self.trigger_type]()

from brain.skills import random_lyrics
from signalbot import Command, Context


class LyricsCommand(Command):
    def describe(self) -> str:
        return "Quotes a random lyric phrase from any given artist"

    async def handle(self, c: Context):
        if "!lyrics" in c.message.text:
            await c.start_typing()

            artist = c.message.text.split("lyrics ", 1)[1]
            response = random_lyrics.get_lyrics(artist)

            await c.stop_typing()
            await c.send(response)

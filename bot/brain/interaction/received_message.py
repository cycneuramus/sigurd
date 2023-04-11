from brain.interaction.triggers import triggers


class RecievedMessage:
    def __init__(self, text: str):
        self.text = text
        self.trigger_type = self.get_trigger_type()
        self.trigger_phrase = self.get_trigger_phrase()
        self.botname_mentioned = self.is_botname_mentioned()

    def is_botname_mentioned(self) -> bool:
        return any(botname in self.text for botname in triggers["botname"])

    def get_trigger_type(self) -> str:
        trigger_type = ""
        for _type, phrases in triggers.items():
            if any(phrase in self.text for phrase in phrases):
                if _type == "botname":
                    continue
                trigger_type = _type
                break
            else:
                continue

        return trigger_type

    def get_trigger_phrase(self) -> str:
        if not self.trigger_type:
            return ""

        trigger_phrase = ""
        for phrase in triggers[self.trigger_type]:
            if phrase in self.text:
                trigger_phrase = phrase
                break

        return trigger_phrase
